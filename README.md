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

De primaire Nederlandse zoekintenties staan in `content/seo-content-plan-nederland.md`. De bijbehorende pagina's worden gegenereerd met:

```bash
python scripts/generate_seo_landing_pages.py
```

Het script maakt de landingspagina's op rootniveau, werkt de kenniscentrum-hub bij en voegt de URL's toe aan `sitemap.xml`. Schrijf deze pagina's als nuchtere uitleg voor Nederlandse investeerders: geen harde rendementsclaims, wel concrete vragen, risico's, bronnen en vervolgstappen.

## Analytics en conversiemeting

Alle HTML-pagina's laden Vercel Web Analytics via `/_vercel/insights/script.js`. In `script.js` worden extra events aangeboden voor:

- CTA-clicks naar contact, gids, projecten en Calendar.
- Succesvolle formulierinzendingen.
- Mislukte formulierinzendingen.
- Gebruik van de ROI-calculator.

Formulierdata blijft leidend in Google Sheets. Analytics is bedoeld om verkeersbronnen, pagina's en conversieroutes te beoordelen, niet als CRM. Let op: Vercel custom events zijn afhankelijk van het Vercel-plan; op de gratis setup blijft Google Sheets daarom de betrouwbare conversieregistratie.

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

Zonder `GOOGLE_APPS_SCRIPT_URL` valt de API terug op SMTP-mail. Dat is alleen fallback; de gewenste productieflow is Google Sheets als CRM-log.
