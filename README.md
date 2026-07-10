# Invest in Bali website

Bronnen van waarheid:

- Websitecode: https://github.com/investinbali/investinbali.nl
- Live website: https://www.investinbali.nl
- Documenten, gidsen, exports en interne plannen: https://drive.google.com/drive/folders/1IzguaF_4bBh6xnYHgn1G8JdgX9Oj6_di
- Hosting/deployments: Vercel project `investinbali`

## Workflow

Websitebestanden horen in GitHub. Wijzigingen aan HTML, CSS, JavaScript, assets voor de website en configuratie worden lokaal aangepast in een Git-working-copy, daarna gecommit en gepusht naar `main`.

Vercel is gekoppeld aan GitHub. Elke push naar `main` maakt automatisch een nieuwe production deployment.

Google Drive is bedoeld voor documenten die niet direct nodig zijn om de website te bouwen of te deployen: gidsen, Word/PDF exports, research, formulierenplannen, interne notities, screenshots en archiefbestanden.

## Niet in GitHub zetten

Zet deze bestanden niet in GitHub:

- wachtwoorden, app passwords of API keys
- exports in `dist/`
- interne documenten in `docs/`
- losse Word-, PDF-, ZIP- of spreadsheetbestanden
- lokale screenshots of ontwerpbestanden

Gebruik Vercel Environment Variables voor secrets.

## Nieuwe teamleden

1. Clone de repository vanuit GitHub.
2. Werk alleen vanuit een lokale Git-working-copy, niet rechtstreeks vanuit Drive als opslagbron.
3. Sla projectdocumentatie op in de gedeelde Google Drive-map.
4. Commit alleen websitebestanden.
5. Push naar `main` wanneer de wijziging klaar is om live te gaan.

## Publiceren

Na een push naar `main`:

1. Vercel start automatisch een deployment.
2. Controleer de deployment in Vercel.
3. Controleer de live website op https://www.investinbali.nl.

## Projectdata

Projecten worden beheerd in `data/projects.json`. Na een wijziging in die data moet het generator-script draaien:

```bash
python scripts/generate_project_pages.py
```

Commit daarna zowel `data/projects.json` als de bijgewerkte HTML in `projecten/`.

## Kenniscentrumartikelen

De uitgebreide kenniscentrumartikelen worden gegenereerd uit de interne rapporten in `docs/knowledge-base-wiki/reports/`.

```bash
python scripts/generate_knowledge_articles.py
```

Het script maakt publieke SEO-artikelen onder `kenniscentrum/`, werkt de wiki-hub bij en voegt de nieuwe URL's toe aan `sitemap.xml`. Publiceer juridische, fiscale of vergunninggevoelige updates alleen nadat de bronstatus en lokale interpretatie opnieuw zijn gecontroleerd.

## Nederlandse SEO-landingspagina's

De primaire Nederlandse zoekintenties staan als Google Doc in Drive: https://docs.google.com/document/d/14KHBGCZw2IPVrlnY4ho8IWH9aZJm4AI-DU9UxgrYgqc. De bijbehorende pagina's worden gegenereerd met:

```bash
python scripts/generate_seo_landing_pages.py
```

Het script maakt de landingspagina's op rootniveau, werkt de kenniscentrum-hub bij en voegt de URL's toe aan `sitemap.xml`. Schrijf deze pagina's als nuchtere uitleg voor Nederlandse investeerders: geen harde rendementsclaims, wel concrete vragen, risico's, bronnen en vervolgstappen.

## Analytics en conversiemeting

Google Analytics 4 wordt centraal geconfigureerd via `analytics-config.js`. Zet daar de GA4 Measurement ID; de huidige live configuratie gebruikt `G-8YTKGPCEWE`. Het Analytics-script wordt pas geladen nadat de bezoeker analytics expliciet heeft geaccepteerd. Die keuze wordt lokaal opgeslagen onder `investinbali_analytics_consent`. De knop `Cookievoorkeuren` in iedere footer trekt de huidige toestemming in, verwijdert bereikbare GA-cookies en opent de keuze opnieuw.

Vercel Web Analytics wordt niet hardcoded geladen. Als Vercel Analytics later in het Vercel-dashboard wordt geactiveerd, controleer dan eerst of `/_vercel/insights/script.js` live een `200` teruggeeft voordat je die loader opnieuw toevoegt. Een niet-geactiveerde Vercel Analytics endpoint geeft `404` en veroorzaakt onnodige browserfouten.

In `script.js` worden extra events aangeboden voor:

- CTA-clicks naar contact, gids, projecten en Calendar.
- Succesvolle formulierinzendingen.
- Mislukte formulierinzendingen.
- Gebruik van de ROI-calculator.
- Funnelstappen zoals `route_select`, `micro_conversion`, `lead_intent`, `generate_lead` en `engaged_read_30s`.

Mislukte formulierinzendingen sturen alleen veilige technische parameters mee: `form_name`, `http_status` en `error_code`, nooit ingevulde persoonsgegevens.

Markeer in GA4 Admin minimaal `generate_lead` en `form_submit_success` als key events zodra deze eventnamen na een echte of gecontroleerde testinzending voor het eerst zijn waargenomen. Ook `qualify_lead`, `download_gids_click`, `schedule_call_click` en `roi_calculator_used` kunnen als key event worden gemarkeerd. Formulierdata blijft leidend in Google Sheets. Analytics is bedoeld om verkeersbronnen, pagina's en conversieroutes te beoordelen, niet als CRM.

## Formulieren en CRM

Alle formulieren posten naar `/api/contact`. De Vercel Function valideert de velden, verrijkt de inzending met `received_at`, `referrer`, `user_agent` en `client_ip`, en stuurt de lead door naar Google Apps Script wanneer `GOOGLE_APPS_SCRIPT_URL` in Vercel is ingesteld.

De Google Apps Script-code staat in `scripts/google-apps-script-form-handler.gs`. Die schrijft iedere inzending naar Google Sheets:

- `Leads`: centrale masterlijst.
- `Call aanvragen`: plan-een-call leads met lead score.
- `Gids aanvragen`: gidsdownloads.
- `Info aanvragen`: gerichte informatievragen via de contactpagina.
- `Updates`: update-inschrijvingen.
- `Log`: technische fouten.

Script properties voor Apps Script:

- `SPREADSHEET_ID`: ID van de CRM Google Sheet.
- `NOTIFY_EMAIL`: `info@investinbali.nl`.
- `CALENDAR_URL`: Google Calendar appointment schedule URL. Current booking page: `https://calendar.app.google/KmYX9vj1hj8wEcLe6`.
- `GUIDE_URL`: URL van de gids-PDF.

Zonder `GOOGLE_APPS_SCRIPT_URL`, of wanneer die endpoint een fout teruggeeft, valt de API terug op SMTP-mail. Zo blijft een aanvraag bereikbaar terwijl de Sheets-koppeling wordt hersteld. De gewenste productieflow blijft Google Sheets als CRM-log; controleer daarom een `email_fallback` respons en herstel de Apps Script-deployment.
