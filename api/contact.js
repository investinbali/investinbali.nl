const nodemailer = require("nodemailer");

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
};

function clean(value) {
  return String(value || "").trim();
}

function label(value) {
  return clean(value).replace(/_/g, " ");
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

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const data = req.body || {};
  const leadType = clean(data.lead_type);
  const required = REQUIRED_FIELDS[leadType];

  if (!required) {
    return res.status(400).json({ error: "Onbekend formulier." });
  }

  const missing = required.filter((field) => !clean(data[field]));
  if (missing.length) {
    return res.status(400).json({ error: "Niet alle verplichte velden zijn ingevuld." });
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
        });
      }

      return res.status(200).json(result);
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
    return res.status(500).json({ error: "Mail is nog niet geconfigureerd." });
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
      replyTo: clean(data.email),
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
      code: err.code || "SMTP_ERROR",
    });
  }

  return res.status(200).json({ ok: true });
};
