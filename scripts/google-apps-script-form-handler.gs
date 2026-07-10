/**
 * Invest in Bali form handler.
 *
 * Deploy this file as a Google Apps Script Web App:
 * - Execute as: Me
 * - Who has access: Anyone
 *
 * Then set the Web App URL in Vercel as:
 * GOOGLE_APPS_SCRIPT_URL=https://script.google.com/macros/s/.../exec
 */

const CONFIG = {
  SPREADSHEET_NAME: "Invest in Bali - Leads",
  SPREADSHEET_ID: "1LRl03IuZ5nIAW9FFMxdpJrERUVVndBqIWp03QxCfLlU",
  NOTIFY_EMAIL: "info@investinbali.nl",
  CALENDAR_URL: "https://calendar.app.google/KmYX9vj1hj8wEcLe6",
  GUIDE_URL: "https://www.investinbali.nl/assets/downloads/gratis-gids-investeren-in-bali-2026.pdf",
};

let cachedSpreadsheet = null;

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

const FLOW_SHEETS = {
  call_aanvraag: "Call aanvragen",
  gids_aanvraag: "Gids aanvragen",
  member_gids_inschrijving: "Gids aanvragen",
  member_inschrijving: "Updates",
  info_aanvraag: "Info aanvragen",
};

const HEADERS = [
  "created_at",
  "lead_id",
  "lead_type",
  "source_page",
  "name",
  "email",
  "phone",
  "interest",
  "segment",
  "budget_range",
  "timeline",
  "investment_goal",
  "experience_level",
  "preferred_area",
  "message",
  "lead_score",
  "lead_status",
  "next_action",
  "calendar_status",
  "calendar_event_id",
  "referrer",
  "user_agent",
  "client_ip",
  "utm_source",
  "utm_medium",
  "utm_campaign",
  "consent",
  "notes",
];

function getConfig(key) {
  return PropertiesService.getScriptProperties().getProperty(key) || CONFIG[key] || "";
}

function doGet() {
  const spreadsheet = getSpreadsheet();

  return jsonResponse({
    ok: true,
    service: "Invest in Bali CRM form handler",
    sheets: true,
    spreadsheet_id: spreadsheet.getId(),
    spreadsheet_url: spreadsheet.getUrl(),
    calendar: Boolean(getConfig("CALENDAR_URL")),
  });
}

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);

  try {
    const data = parsePayload(e);
    const leadType = clean(data.lead_type);
    validatePayload(leadType, data);

    const lead = buildLead(data, leadType);
    appendLead("Leads", lead);
    const deliveryWarnings = [];

    runOptionalStep("flow_sheet", lead, deliveryWarnings, function () {
      appendLead(FLOW_SHEETS[leadType], lead);
    });
    runOptionalStep("internal_notification", lead, deliveryWarnings, function () {
      sendInternalNotification(lead);
    });

    if (leadType === "gids_aanvraag" || leadType === "member_gids_inschrijving") {
      runOptionalStep("guide_email", lead, deliveryWarnings, function () {
        sendGuideEmail(lead);
      });
    }

    if (leadType === "member_inschrijving") {
      runOptionalStep("update_confirmation", lead, deliveryWarnings, function () {
        sendUpdateConfirmation(lead);
      });
    }

    if (leadType === "info_aanvraag") {
      runOptionalStep("info_confirmation", lead, deliveryWarnings, function () {
        sendInfoConfirmation(lead);
      });
    }

    return jsonResponse({
      ok: true,
      lead_id: lead.lead_id,
      next_step: leadType === "call_aanvraag" ? "calendar" : "done",
      calendar_url: leadType === "call_aanvraag" ? getConfig("CALENDAR_URL") : "",
      delivery_status: deliveryWarnings.length ? "stored_with_warnings" : "complete",
    });
  } catch (err) {
    logError(err, e);
    return jsonResponse({
      ok: false,
      error:
        "Aanvraag is niet opgeslagen. Probeer later opnieuw of mail info@investinbali.nl.",
    });
  } finally {
    lock.releaseLock();
  }
}

function parsePayload(e) {
  if (!e || !e.postData || !e.postData.contents) {
    throw new Error("Missing request body");
  }

  return JSON.parse(e.postData.contents);
}

function validatePayload(leadType, data) {
  const required = REQUIRED_FIELDS[leadType];

  if (!required) {
    throw new Error("Unknown lead_type: " + leadType);
  }

  const missing = required.filter(function (field) {
    return !clean(data[field]);
  });

  if (missing.length) {
    throw new Error("Missing required fields: " + missing.join(", "));
  }

  if (!isValidEmail(data.email)) {
    throw new Error("Invalid email");
  }
}

function buildLead(data, leadType) {
  const now = new Date();
  const leadScore = leadType === "call_aanvraag" ? calculateLeadScore(data) : "";

  return {
    created_at: now.toISOString(),
    lead_id: createLeadId(now),
    lead_type: leadType,
    source_page: clean(data.source_page || data.page_source),
    name: clean(data.name),
    email: clean(data.email),
    phone: clean(data.phone),
    interest: clean(data.interest),
    segment: clean(data.segment),
    budget_range: clean(data.budget_range),
    timeline: clean(data.timeline),
    investment_goal: clean(data.investment_goal),
    experience_level: clean(data.experience_level),
    preferred_area: clean(data.preferred_area),
    message: clean(data.message),
    lead_score: leadScore,
    lead_status: leadType === "call_aanvraag" ? statusFromScore(leadScore) : "new",
    next_action: leadType === "call_aanvraag" ? "Plan call via Google Calendar" : "Follow up",
    calendar_status: leadType === "call_aanvraag" ? "calendar_link_sent" : "",
    calendar_event_id: "",
    referrer: clean(data.referrer),
    user_agent: clean(data.user_agent),
    client_ip: clean(data.client_ip),
    utm_source: clean(data.utm_source),
    utm_medium: clean(data.utm_medium),
    utm_campaign: clean(data.utm_campaign),
    consent: clean(data.consent),
    notes: "",
  };
}

function appendLead(sheetName, lead) {
  if (!sheetName) {
    throw new Error("Missing sheet name");
  }

  const sheet = getOrCreateSheet(sheetName);
  ensureHeaders(sheet);
  sheet.appendRow(HEADERS.map(function (header) {
    return lead[header] || "";
  }));
}

function getOrCreateSheet(sheetName) {
  const spreadsheet = getSpreadsheet();
  return spreadsheet.getSheetByName(sheetName) || spreadsheet.insertSheet(sheetName);
}

function getSpreadsheet() {
  if (cachedSpreadsheet) {
    return cachedSpreadsheet;
  }

  const properties = PropertiesService.getScriptProperties();
  const savedId = properties.getProperty("SPREADSHEET_ID");
  const configuredId = getConfig("SPREADSHEET_ID");
  const spreadsheetId = savedId || configuredId;

  if (spreadsheetId) {
    try {
      cachedSpreadsheet = SpreadsheetApp.openById(spreadsheetId);
      properties.setProperty("SPREADSHEET_ID", cachedSpreadsheet.getId());
      return cachedSpreadsheet;
    } catch (err) {
      console.error("Unable to open configured spreadsheet. Creating a new CRM sheet.", err);
    }
  }

  cachedSpreadsheet = SpreadsheetApp.create(getConfig("SPREADSHEET_NAME"));
  properties.setProperty("SPREADSHEET_ID", cachedSpreadsheet.getId());
  initialiseSpreadsheet(cachedSpreadsheet);
  return cachedSpreadsheet;
}

function initialiseSpreadsheet(spreadsheet) {
  const defaultSheet = spreadsheet.getSheets()[0];
  if (defaultSheet && defaultSheet.getName() !== "Leads") {
    defaultSheet.setName("Leads");
  }

  const sheetNames = ["Leads", "Call aanvragen", "Gids aanvragen", "Updates", "Info aanvragen", "Log"];
  sheetNames.forEach(function (sheetName) {
    const sheet = spreadsheet.getSheetByName(sheetName) || spreadsheet.insertSheet(sheetName);
    if (sheetName === "Log") {
      const logHeaders = ["created_at", "lead_id", "flow", "status", "message", "raw_payload"];
      const currentHeaders = sheet.getRange(1, 1, 1, logHeaders.length).getValues()[0];
      const hasHeaders = currentHeaders.some(function (value) {
        return clean(value);
      });

      if (!hasHeaders) {
        sheet.getRange(1, 1, 1, logHeaders.length).setValues([logHeaders]);
        sheet.setFrozenRows(1);
      }
      return;
    }

    ensureHeaders(sheet);
  });
}

function ensureHeaders(sheet) {
  const currentHeaders = sheet.getRange(1, 1, 1, HEADERS.length).getValues()[0];
  const hasHeaders = currentHeaders.some(function (value) {
    return clean(value);
  });

  if (!hasHeaders) {
    sheet.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
    sheet.setFrozenRows(1);
  }
}

function sendInternalNotification(lead) {
  const subject = "Nieuwe aanvraag via Invest in Bali: " + lead.lead_type;
  const body = [
    "Nieuwe lead via investinbali.nl",
    "",
    "Lead ID: " + lead.lead_id,
    "Type: " + lead.lead_type,
    "Naam: " + lead.name,
    "E-mail: " + lead.email,
    "Telefoon: " + lead.phone,
    "Doel: " + lead.investment_goal,
    "Budget: " + lead.budget_range,
    "Tijdlijn: " + lead.timeline,
    "Ervaring: " + lead.experience_level,
    "Regio: " + lead.preferred_area,
    "Interesse: " + lead.interest,
    "Segment: " + lead.segment,
    "Score: " + lead.lead_score,
    "Status: " + lead.lead_status,
    "",
    "Bericht:",
    lead.message,
  ].join("\n");

  MailApp.sendEmail(getConfig("NOTIFY_EMAIL"), subject, body, {
    replyTo: lead.email,
    name: "Invest in Bali website",
  });
}

function sendGuideEmail(lead) {
  const subject = "Je gids investeren in Bali 2026";
  const body = [
    "Hallo " + lead.name + ",",
    "",
    'Bedankt voor je aanvraag. Hierbij ontvang je de gids "Investeren in Bali 2026".',
    "",
    "In de gids lees je waar je op moet letten bij huizen kopen op Bali, hoe leasehold werkt, wanneer een PT PMA relevant kan zijn, waarom zoning belangrijk is en hoe je bruto rendement realistischer vertaalt naar netto resultaat.",
    "",
    "Download de gids hier:",
    getConfig("GUIDE_URL"),
    "",
    "Wil je na het lezen jouw situatie bespreken? Plan dan een call:",
    getConfig("CALENDAR_URL"),
    "",
    "Met vriendelijke groet,",
    "Invest in Bali",
  ].join("\n");

  MailApp.sendEmail(lead.email, subject, body, {
    name: "Invest in Bali",
  });
}

function sendUpdateConfirmation(lead) {
  const subject = "Je staat op de lijst voor Invest in Bali updates";
  const body = [
    "Hallo " + lead.name + ",",
    "",
    "Bedankt voor je inschrijving. We sturen je relevante updates over huizen op Bali, marktinzichten en nieuwe content.",
    "",
    "Wil je jouw situatie eerder bespreken? Plan dan een call:",
    getConfig("CALENDAR_URL"),
    "",
    "Met vriendelijke groet,",
    "Invest in Bali",
  ].join("\n");

  MailApp.sendEmail(lead.email, subject, body, {
    name: "Invest in Bali",
  });
}

function sendInfoConfirmation(lead) {
  const subject = "We hebben je vraag ontvangen";
  const body = [
    "Hallo " + lead.name + ",",
    "",
    "Bedankt voor je vraag over Invest in Bali. We bekijken je bericht en reageren met een gerichte vervolgstap.",
    "",
    "Je vraag:",
    lead.message,
    "",
    "Wil je direct jouw situatie bespreken? Plan dan een call:",
    getConfig("CALENDAR_URL"),
    "",
    "Met vriendelijke groet,",
    "Invest in Bali",
  ].join("\n");

  MailApp.sendEmail(lead.email, subject, body, {
    name: "Invest in Bali",
  });
}

function calculateLeadScore(data) {
  let score = 0;

  if (data.budget_range === "500k_plus" || data.budget_range === "300k_500k") {
    score += 2;
  } else if (data.budget_range === "150k_300k") {
    score += 1;
  }

  if (data.timeline === "0_3_maanden") {
    score += 3;
  } else if (data.timeline === "3_6_maanden") {
    score += 2;
  } else if (data.timeline === "6_12_maanden") {
    score += 1;
  }

  if (data.investment_goal === "short_stay" || data.investment_goal === "combinatie") {
    score += 1;
  }

  if (data.experience_level === "objecten_bekeken") {
    score += 2;
  } else if (data.experience_level === "onderzoek_gedaan" || data.experience_level === "eerder_vastgoed_gekocht") {
    score += 1;
  }

  if (clean(data.phone)) {
    score += 1;
  }

  return score;
}

function statusFromScore(score) {
  if (score >= 6) {
    return "qualified";
  }
  if (score >= 3) {
    return "needs_follow_up";
  }
  return "new";
}

function logError(err, event) {
  try {
    const sheet = getOrCreateSheet("Log");
    const headers = ["created_at", "lead_id", "flow", "status", "message", "raw_payload"];
    const currentHeaders = sheet.getRange(1, 1, 1, headers.length).getValues()[0];
    const hasHeaders = currentHeaders.some(function (value) {
      return clean(value);
    });

    if (!hasHeaders) {
      sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
      sheet.setFrozenRows(1);
    }

    sheet.appendRow([
      new Date().toISOString(),
      "",
      "form_submit",
      "error",
      err.message,
      "",
    ]);
  } catch (logErr) {
    console.error(logErr);
  }
}

function runOptionalStep(flow, lead, warnings, callback) {
  try {
    callback();
  } catch (err) {
    warnings.push(flow);
    logDeliveryWarning(flow, lead.lead_id, err);
  }
}

function logDeliveryWarning(flow, leadId, err) {
  try {
    const sheet = getOrCreateSheet("Log");
    sheet.appendRow([
      new Date().toISOString(),
      leadId,
      flow,
      "warning",
      err && err.message ? String(err.message).slice(0, 500) : "Unknown delivery warning",
      "",
    ]);
  } catch (logErr) {
    console.error(logErr);
  }
}

function createLeadId(date) {
  const timePart = Utilities.formatDate(date, Session.getScriptTimeZone(), "yyyyMMdd-HHmmss");
  const randomPart = Math.floor(Math.random() * 9000 + 1000);
  return "IIB-" + timePart + "-" + randomPart;
}

function clean(value) {
  return String(value || "").trim();
}

function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(clean(value));
}

function jsonResponse(payload) {
  return ContentService.createTextOutput(JSON.stringify(payload)).setMimeType(
    ContentService.MimeType.JSON
  );
}
