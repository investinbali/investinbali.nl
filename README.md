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

