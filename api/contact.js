const nodemailer = require("nodemailer");

const CALENDAR_URL = process.env.CALENDAR_URL || "https://calendar.app.google/KmYX9vj1hj8wEcLe6";
const MAX_BODY_BYTES = 32 * 1024;
const DEFAULT_FIELD_LIMIT = 200;
const FIELD_LIMITS = {
  email: 254,
  phone: 40,
  message: 3000,
  user_agent: 500,
  referrer: 1000,
  page_source: 1000,
  website: 200,
};

const REQUIRED_FIELDS = {
  call_aanvraag: [
    "name",
    "email",
    "phone",
    "investment_goal",
    "budget_range",
    "timeline",
    "experience_level",
    "message",
    "consent",
  ],
  gids_aanvraag: ["name", "email", "interest", "consent"],
  member_gids_inschrijving: ["name", "email", "interest", "consent"],
  member_inschrijving: ["name", "email", "segment", "consent"],
  info_aanvraag: ["name", "email", "segment", "message", "consent"],
};

function clean(value) {
  return String(value || "").trim();
}

function cleanHeader(value) {
  return clean(value).replace(/[\r\n]+/g, " ");
}

function isValidEmail(value) {
  const email = cleanHeader(value);
  return email.length <= FIELD_LIMITS.email && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validateAndCleanPayload(body) {
  if (!body || typeof body !== "object" || Array.isArray(body)) {
    return { error: "Ongeldige aanvraag.", code: "INVALID_PAYLOAD" };
  }

  let encodedLength;
  try {
    encodedLength = Buffer.byteLength(JSON.stringify(body), "utf8");
  } catch (_error) {
    return { error: "Ongeldige aanvraag.", code: "INVALID_PAYLOAD" };
  }
  if (encodedLength > MAX_BODY_BYTES) {
    return { error: "De aanvraag is te groot.", code: "PAYLOAD_TOO_LARGE" };
  }

  const data = {};
  for (const [key, rawValue] of Object.entries(body)) {
    if (typeof rawValue !== "string" && typeof rawValue !== "number" && typeof rawValue !== "boolean") {
      return { error: "Ongeldige veldwaarde.", code: "INVALID_FIELD" };
    }
    const value = clean(rawValue);
    const limit = FIELD_LIMITS[key] || DEFAULT_FIELD_LIMIT;
    if (value.length > limit) {
      return { error: "Een of meer velden zijn te lang.", code: "INVALID_FIELD" };
    }
    data[key] = value;
  }
  return { data };
}

function label(value) {
  return cleanHeader(value).replace(/_/g, " ");
}

function buildMessage(data) {
  const leadType = clean(data.lead_type) || "formulier";
  const rows = [
    ["Type", leadType],
    ["Pagina", data.page_source],
    ["Naam", data.name],
    ["E-mail", data.email],
    ["Telefoon", data.phone],
    ["Interesse", data.interest],
    ["Segment", data.segment],
    ["Doel", data.investment_goal],
    ["Budget", data.budget_range],
    ["Tijdlijn", data.timeline],
    ["Ervaring", data.experience_level],
    ["Regio", data.preferred_area],
    ["Bericht", data.message],
    ["Consent", data.consent],
  ].filter(([, value]) => clean(value));

  return rows.map(([key, value]) => `${key}: ${clean(value)}`).join("\n");
}

function getClientIp(req) {
  return clean(req.headers["x-forwarded-for"]).split(",")[0] || clean(req.socket?.remoteAddress);
}

function enrichPayload(req, data) {
  return {
    ...data,
    received_at: new Date().toISOString(),
    user_agent: clean(req.headers["user-agent"]).slice(0, FIELD_LIMITS.user_agent),
    referrer: clean(req.headers.referer || req.headers.referrer).slice(0, FIELD_LIMITS.referrer),
    client_ip: getClientIp(req),
  };
}

function addFlowLinks(leadType, result = {}) {
  return {
    ...result,
    calendar_url: leadType === "call_aanvraag" ? result.calendar_url || CALENDAR_URL : result.calendar_url || "",
  };
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed", code: "METHOD_NOT_ALLOWED" });
  }

  const contentLength = Number(req.headers["content-length"] || 0);
  if (contentLength > MAX_BODY_BYTES) {
    return res.status(413).json({ error: "De aanvraag is te groot.", code: "PAYLOAD_TOO_LARGE" });
  }

  const validated = validateAndCleanPayload(req.body || {});
  if (validated.error) {
    const status = validated.code === "PAYLOAD_TOO_LARGE" ? 413 : 400;
    return res.status(status).json({ error: validated.error, code: validated.code });
  }
  if (clean(validated.data.website)) {
    // Do not reveal bot detection; legitimate clients never fill this field.
    return res.status(200).json({ ok: true });
  }

  const data = enrichPayload(req, validated.data);
  const leadType = clean(data.lead_type);
  const required = REQUIRED_FIELDS[leadType];

  if (!required) {
    return res.status(400).json({ error: "Onbekend formulier.", code: "INVALID_FIELD" });
  }

  const missing = required.filter((field) => !clean(data[field]));
  if (missing.length) {
    return res.status(400).json({
      error: "Niet alle verplichte velden zijn ingevuld.",
      code: "MISSING_REQUIRED_FIELDS",
    });
  }

  if (!isValidEmail(data.email)) {
    return res.status(400).json({ error: "Vul een geldig e-mailadres in.", code: "INVALID_EMAIL" });
  }

  if (process.env.GOOGLE_APPS_SCRIPT_URL) {
    try {
      const googleResponse = await fetch(process.env.GOOGLE_APPS_SCRIPT_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const responseText = await googleResponse.text();
      const result = responseText ? JSON.parse(responseText) : { ok: true };

      if (!googleResponse.ok || result.ok === false) {
        return res.status(502).json({
          error:
            result.error ||
            "Aanvraag is niet opgeslagen. Probeer later opnieuw of mail info@investinbali.nl.",
          code: "GOOGLE_APPS_SCRIPT_ERROR",
        });
      }

      return res.status(200).json({
        ok: true,
        crm: "google_sheets",
        ...addFlowLinks(leadType, result),
      });
    } catch (err) {
      console.error("Google Apps Script submit failed", {
        message: err.message,
      });

      return res.status(502).json({
        error:
          "Aanvraag is niet opgeslagen. Probeer later opnieuw of mail info@investinbali.nl.",
        code: "GOOGLE_APPS_SCRIPT_ERROR",
      });
    }
  }

  if (!process.env.SMTP_USER || !process.env.SMTP_PASS) {
    return res.status(500).json({
      error: "Mail is nog niet geconfigureerd.",
      code: "MAIL_NOT_CONFIGURED",
    });
  }

  const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST || "smtp.gmail.com",
    port: Number(process.env.SMTP_PORT || 465),
    secure: String(process.env.SMTP_SECURE || "true") === "true",
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS,
    },
  });

  const subject = `Nieuwe aanvraag via Invest in Bali: ${label(leadType)}`;
  const text = buildMessage(data);

  try {
    await transporter.sendMail({
      from: `"Invest in Bali website" <${process.env.SMTP_USER}>`,
      to: process.env.LEAD_TO_EMAIL || "info@investinbali.nl",
      replyTo: cleanHeader(data.email),
      subject,
      text,
    });
  } catch (err) {
    console.error("Mail send failed", {
      code: err.code,
      command: err.command,
      responseCode: err.responseCode,
      response: err.response,
    });

    return res.status(502).json({
      error:
        "Mailserver kon de aanvraag niet verzenden. Mail ons direct via info@investinbali.nl.",
      code: "MAIL_SEND_ERROR",
    });
  }

  return res.status(200).json(addFlowLinks(leadType, { ok: true, crm: "email_only" }));
};
