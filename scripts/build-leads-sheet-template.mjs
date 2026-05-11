import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputPath = "dist/invest-in-bali-leads-template.xlsx";

const headers = [
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
  "utm_source",
  "utm_medium",
  "utm_campaign",
  "consent",
  "notes",
];

const logHeaders = ["created_at", "lead_id", "flow", "status", "message", "raw_payload"];

function formatSheet(sheet, width = headers.length) {
  const headerRange = sheet.getRangeByIndexes(0, 0, 1, width);
  headerRange.format = {
    fill: "#4b2f1d",
    font: { bold: true, color: "#ffffff" },
    wrapText: true,
  };
  sheet.freezePanes.freezeRows(1);
  sheet.getRangeByIndexes(0, 0, 1, width).format.rowHeightPx = 36;
  sheet.getRangeByIndexes(0, 0, 200, width).format.wrapText = true;
}

const workbook = Workbook.create();

for (const sheetName of ["Leads", "Call aanvragen", "Gids aanvragen", "Updates"]) {
  const sheet = workbook.worksheets.add(sheetName);
  sheet.getRangeByIndexes(0, 0, 1, headers.length).values = [headers];
  formatSheet(sheet);
}

const logSheet = workbook.worksheets.add("Log");
logSheet.getRangeByIndexes(0, 0, 1, logHeaders.length).values = [logHeaders];
formatSheet(logSheet, logHeaders.length);

const instructions = workbook.worksheets.add("Uitleg");
instructions.getRange("A1").values = [["Invest in Bali - Leads"]];
instructions.getRange("A2").values = [["Deze Google Sheet is bedoeld als eerste lead-database voor de formulieren op investinbali.nl."]];
instructions.getRange("A4").values = [["Tabs"]];
instructions.getRange("A5:B9").values = [
  ["Leads", "Centrale masterlijst met alle formulierinzendingen."],
  ["Call aanvragen", "Alle aanvragen voor een kennismakingscall met kwalificatievelden en score."],
  ["Gids aanvragen", "Alle gids-download leads."],
  ["Updates", "Alle inschrijvingen voor markt- en projectupdates."],
  ["Log", "Technische logging vanuit Apps Script."],
];
instructions.getRange("A11").values = [["Volgende stap"]];
instructions.getRange("A12").values = [["Kopieer het spreadsheet-ID uit de URL en plaats dit in scripts/google-apps-script-form-handler.gs bij CONFIG.SPREADSHEET_ID."]];
instructions.getRange("A1:B1").format = {
  fill: "#d8a451",
  font: { bold: true, color: "#161311" },
};
instructions.getRange("A4:B4").format = {
  fill: "#4b2f1d",
  font: { bold: true, color: "#ffffff" },
};
instructions.getRange("A11:B11").format = {
  fill: "#4b2f1d",
  font: { bold: true, color: "#ffffff" },
};
instructions.getRange("A1:B12").format.wrapText = true;
instructions.freezePanes.freezeRows(1);

await fs.mkdir("dist", { recursive: true });
const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(outputPath);

console.log(outputPath);
