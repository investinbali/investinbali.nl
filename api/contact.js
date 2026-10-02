const nodemailer = require("nodemailer");
const { createHash } = require("node:crypto");

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
    "consent",
  ],
  gids_aanvraag: ["email", "consent"],
  member_gids_inschrijving: ["email", "consent"],
  member_inschrijving: ["name", "email", "segment", "consent"],
  info_aanvraag: ["name", "email", "segment", "message", "consent"],
};

// Best-effort per warm instance. A distributed edge/WAF limit is still required
// for protection across instances; never present this as a global quota.
const requestWindows = new Map();
const WINDOW_MS = 15 * 60 * 1000;
function rateLimited(req) {
  const ip = getClientIp(req);
  if (!ip) return false;
  const now = Date.now();
  for (const [key, value] of requestWindows) {
    if (value.expires <= now) requestWindows.delete(key);
  }
  const key = createHash("sha256").update(ip).digest("hex");
  const entry = requestWindows.get(key) || { count: 0, expires: now + WINDOW_MS };
  if (entry.count >= 5) return true;
  if (!requestWindows.has(key) && requestWindows.size >= 10000) return true;
  entry.count += 1;
  requestWindows.set(key, entry);
  return false;
}

function confirmed(value) { return ["yes", "true", "1"].includes(clean(value)); }

function upstreamPayload(data) {
  const result = { ...data };
  // Older deployed Apps Script handlers require these fields. Explicit missing
  // labels preserve compatibility without inventing visitor answers.
  const optional = data.lead_type === "call_aanvraag"
    ? ["investment_goal", "budget_range", "timeline", "experience_level", "message"]
    : ["gids_aanvraag", "member_gids_inschrijving"].includes(data.lead_type) ? ["name", "interest"] : [];
  optional.forEach((field) => { if (!result[field]) result[field] = "Niet opgegeven"; });
  result.consent = `request=yes; marketing=${result.marketing_consent}; version=2026-10-02`;
  return result;
}

function clean(value) {
  return String(value || "").trim();
}

function cleanHeader(value) {
  return clean(value).replace(/[\r\n]+/g, " ");
}

function isValidEmail(value) {
  if (/[\r\n]/.test(String(value))) return false;
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
    ["Updates toestemming", data.marketing_consent],
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
  const isGuide = ["gids_aanvraag", "member_gids_inschrijving"].includes(leadType);
  return {
    ...result,
    ...(isGuide ? {
      guide_url: "/assets/downloads/gratis-gids-investeren-in-bali-2026.pdf?v=20261002",
      // Provider acceptance is not proof of inbox delivery. Older handlers report only aggregate status.
      guide_email_status: result.guide_email_status === "accepted" || (!result.guide_email_status && result.delivery_status === "complete") ? "accepted" : "unconfirmed",
    } : {}),
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

  if (!confirmed(data.consent)) {
    return res.status(400).json({ error: "Bevestig toestemming voor deze aanvraag.", code: "CONSENT_REQUIRED" });
  }
  if (data.marketing_consent && !["yes", "no", "true", "false", "1", "0"].includes(data.marketing_consent)) {
    return res.status(400).json({ error: "Ongeldige updatekeuze.", code: "INVALID_FIELD" });
  }
  data.marketing_consent = confirmed(data.marketing_consent) || leadType === "member_inschrijving" ? "yes" : "no";
  if (data.phone && (!/^\+?[\d\s().-]+$/.test(data.phone) || !/^\d{7,15}$/.test(data.phone.replace(/\D/g, "")))) {
    return res.status(400).json({ error: "Vul een geldig telefoonnummer met landcode in.", code: "INVALID_PHONE" });
  }
  if (rateLimited(req)) {
    res.setHeader("Retry-After", "900");
    return res.status(429).json({ error: "Te veel aanvragen. Probeer over 15 minuten opnieuw.", code: "RATE_LIMITED" });
  }
  const deliveryData = upstreamPayload(data);

  let googleAppsScriptFailed = false;

  if (process.env.GOOGLE_APPS_SCRIPT_URL) {
    try {
      const googleResponse = await fetch(process.env.GOOGLE_APPS_SCRIPT_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(deliveryData),
        signal: AbortSignal.timeout(15000),
      });

      const responseText = await googleResponse.text();
      const result = responseText ? JSON.parse(responseText) : {};

      if (!googleResponse.ok || result.ok !== true) {
        googleAppsScriptFailed = true;
        console.error("Google Apps Script rejected submission", {
          status: googleResponse.status,
          upstream_ok: result.ok,
        });
      } else {
        return res.status(200).json({
          ok: true,
          crm: "google_sheets",
          ...addFlowLinks(leadType, result),
        });
      }
    } catch (err) {
      googleAppsScriptFailed = true;
      console.error("Google Apps Script submit failed", {
        message: err.message,
      });
    }
  }

  if (!process.env.SMTP_USER || !process.env.SMTP_PASS) {
    if (googleAppsScriptFailed) {
      return res.status(502).json({
        error:
          "Aanvraag is niet opgeslagen. Probeer later opnieuw of mail info@investinbali.nl.",
        code: "GOOGLE_APPS_SCRIPT_ERROR",
      });
    }
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
    connectionTimeout: 10000,
    socketTimeout: 15000,
  });

  const subject = `Nieuwe aanvraag via Invest in Bali: ${label(leadType)}`;
  const text = buildMessage(deliveryData);

  try {
    const sent = await transporter.sendMail({
      from: `"Invest in Bali website" <${process.env.SMTP_USER}>`,
      to: process.env.LEAD_TO_EMAIL || "info@investinbali.nl",
      replyTo: cleanHeader(data.email),
      subject,
      text,
    });
    if (!sent.accepted?.length) throw new Error("Notification was not accepted");
  } catch (err) {
    console.error("Mail send failed", {
      code: err.code,
      command: err.command,
      responseCode: err.responseCode,
    });

    return res.status(502).json({
      error:
        "Mailserver kon de aanvraag niet verzenden. Mail ons direct via info@investinbali.nl.",
      code: "MAIL_SEND_ERROR",
    });
  }

  let guideEmailStatus = "unconfirmed";
  if (["gids_aanvraag", "member_gids_inschrijving"].includes(leadType)) {
    try {
      const sent = await transporter.sendMail({
        from: `"Invest in Bali" <${process.env.SMTP_USER}>`,
        to: cleanHeader(data.email),
        subject: "Je gids investeren in Bali 2026",
        text: "Bedankt voor je aanvraag. Download je gids via:\nhttps://www.investinbali.nl/assets/downloads/gratis-gids-investeren-in-bali-2026.pdf?v=20261002\n\nDit is de door jou aangevraagde gids. Voor vragen: info@investinbali.nl.\nPrivacy: https://www.investinbali.nl/privacybeleid/",
      });
      if (sent.accepted?.some((email) => String(email).toLowerCase() === data.email.toLowerCase())) guideEmailStatus = "accepted";
    } catch (err) {
      // The internal notification already succeeded: do not ask for duplicate submissions.
      console.error("Guide email failed", { code: err.code, responseCode: err.responseCode });
    }
  }

  return res.status(200).json(
    addFlowLinks(leadType, {
      ok: true,
      crm: googleAppsScriptFailed ? "email_fallback" : "email_only",
      guide_email_status: guideEmailStatus,
    })
  );
};
