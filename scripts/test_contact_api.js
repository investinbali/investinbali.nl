const assert = require("node:assert/strict");
const Module = require("node:module");

// The validation tests do not send mail. Keep them runnable before npm install.
const originalLoad = Module._load;
let mailShouldFail = false;
Module._load = function mockedLoad(request, parent, isMain) {
  if (request === "nodemailer") {
    return {
      createTransport: () => ({
        sendMail: async () => {
          if (mailShouldFail) throw new Error("mock mail failure");
          return { accepted: ["test@example.com"] };
        },
      }),
    };
  }
  return originalLoad.call(this, request, parent, isMain);
};

const handler = require("../api/contact");

async function invoke(body, headers = {}, method = "POST") {
  let statusCode = 200;
  let payload;
  const req = { method, body, headers, socket: {} };
  const res = {
    setHeader() {},
    status(code) {
      statusCode = code;
      return this;
    },
    json(value) {
      payload = value;
      return this;
    },
  };
  await handler(req, res);
  return { statusCode, payload };
}

async function main() {
  const originalFetch = global.fetch;
  const originalUrl = process.env.GOOGLE_APPS_SCRIPT_URL;
  process.env.GOOGLE_APPS_SCRIPT_URL = "https://example.invalid/form-handler";
  global.fetch = async (_url, options) => {
    const submitted = JSON.parse(options.body);
    assert.equal(submitted.email, "test@example.com");
    return { ok: true, text: async () => JSON.stringify({ ok: true }) };
  };

  const valid = await invoke({
    lead_type: "gids_aanvraag",
    name: "Test",
    email: "test@example.com",
    interest: "oriëntatie",
    consent: "yes",
    website: "",
  });
  assert.equal(valid.statusCode, 200);
  assert.equal(valid.payload.ok, true);
  assert.equal(valid.payload.crm, "google_sheets");

  const invalidEmail = await invoke({
    lead_type: "gids_aanvraag",
    name: "Test",
    email: "not-an-email",
    interest: "oriëntatie",
    consent: "yes",
  });
  assert.equal(invalidEmail.statusCode, 400);
  assert.equal(invalidEmail.payload.code, "INVALID_EMAIL");

  const honeypot = await invoke({
    lead_type: "gids_aanvraag",
    name: "Bot",
    email: "bot@example.com",
    interest: "x",
    consent: "yes",
    website: "filled",
  });
  assert.equal(honeypot.statusCode, 200);

  const oversizedField = await invoke({
    lead_type: "gids_aanvraag",
    name: "x".repeat(201),
    email: "test@example.com",
    interest: "x",
    consent: "yes",
  });
  assert.equal(oversizedField.statusCode, 400);
  assert.equal(oversizedField.payload.code, "INVALID_FIELD");

  const missing = await invoke({ lead_type: "gids_aanvraag", email: "test@example.com" });
  assert.equal(missing.statusCode, 400);
  assert.equal(missing.payload.code, "MISSING_REQUIRED_FIELDS");

  const wrongMethod = await invoke({}, {}, "GET");
  assert.equal(wrongMethod.statusCode, 405);
  assert.equal(wrongMethod.payload.code, "METHOD_NOT_ALLOWED");

  const tooLarge = await invoke({}, { "content-length": String(33 * 1024) });
  assert.equal(tooLarge.statusCode, 413);
  assert.equal(tooLarge.payload.code, "PAYLOAD_TOO_LARGE");

  global.fetch = async () => ({
    ok: false,
    text: async () => JSON.stringify({ ok: false, error: "upstream failed" }),
  });
  const downstreamFailure = await invoke({
    lead_type: "gids_aanvraag",
    name: "Test",
    email: "test@example.com",
    interest: "oriëntatie",
    consent: "yes",
  });
  assert.equal(downstreamFailure.statusCode, 502);
  assert.equal(downstreamFailure.payload.code, "GOOGLE_APPS_SCRIPT_ERROR");

  const invalidPayload = await invoke({
    lead_type: "gids_aanvraag",
    name: { nested: true },
    email: "test@example.com",
    interest: "x",
    consent: "yes",
  });
  assert.equal(invalidPayload.statusCode, 400);
  assert.equal(invalidPayload.payload.code, "INVALID_FIELD");

  delete process.env.GOOGLE_APPS_SCRIPT_URL;
  delete process.env.SMTP_USER;
  delete process.env.SMTP_PASS;
  const mailNotConfigured = await invoke({
    lead_type: "gids_aanvraag",
    name: "Test",
    email: "test@example.com",
    interest: "x",
    consent: "yes",
  });
  assert.equal(mailNotConfigured.statusCode, 500);
  assert.equal(mailNotConfigured.payload.code, "MAIL_NOT_CONFIGURED");

  process.env.SMTP_USER = "test@example.com";
  process.env.SMTP_PASS = "secret";
  mailShouldFail = true;
  const originalConsoleError = console.error;
  console.error = () => {};
  const mailFailure = await invoke({
    lead_type: "gids_aanvraag",
    name: "Test",
    email: "test@example.com",
    interest: "x",
    consent: "yes",
  });
  assert.equal(mailFailure.statusCode, 502);
  assert.equal(mailFailure.payload.code, "MAIL_SEND_ERROR");
  console.error = originalConsoleError;
  mailShouldFail = false;
  delete process.env.SMTP_USER;
  delete process.env.SMTP_PASS;

  global.fetch = originalFetch;
  if (originalUrl === undefined) delete process.env.GOOGLE_APPS_SCRIPT_URL;
  else process.env.GOOGLE_APPS_SCRIPT_URL = originalUrl;
  console.log("Contact API valid and invalid path checks passed.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
