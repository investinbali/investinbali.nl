from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from generate_knowledge_articles import BASE_URL, esc, footer, header

ROOT = Path(__file__).resolve().parents[1]
TODAY = date.today().isoformat()
MONTHS_NL = [
    "januari",
    "februari",
    "maart",
    "april",
    "mei",
    "juni",
    "juli",
    "augustus",
    "september",
    "oktober",
    "november",
    "december",
]
UPDATED_LABEL = f"{date.today().day} {MONTHS_NL[date.today().month - 1]} {date.today().year}"


PAGES = [
    {
        "slug": "pbg-slf-bali",
        "title": "PBG en SLF Bali vastgoed",
        "h1": "PBG en SLF op Bali: waarom bouwvergunningen ertoe doen",
        "keyword": "PBG SLF Bali vastgoed",
        "description": "Praktische uitleg over PBG en SLF op Bali: wanneer ze relevant zijn, wat je controleert en waarom vergunningen invloed hebben op risico en verhuurbaarheid.",
        "short": "PBG en SLF zijn belangrijke controlepunten bij Bali vastgoed. Ze zeggen iets over bouwtoestemming, technische oplevering en gebruik van een gebouw. Controleer ze per object voordat je rekent op verhuur, doorverkoop of probleemloos gebruik.",
        "sections": [
            (
                "Wat betekenen PBG en SLF?",
                [
                    "PBG gaat over toestemming om te bouwen of te verbouwen volgens de geldende regels. SLF gaat over de geschiktheid van een gebouw voor gebruik na oplevering.",
                    "Voor kopers is vooral belangrijk of de papieren passen bij het feitelijke gebouw. Een villa kan er af uitzien, maar toch vergunningstechnisch zwak zijn.",
                ],
            ),
            (
                "Waarom dit relevant is voor investeerders",
                [
                    "Vergunningen kunnen invloed hebben op financierbaarheid, verzekering, verhuur, beheer, verkoopbaarheid en risico bij controles.",
                    "Bij nieuwbouw wil je niet alleen renders en planning zien, maar ook wie verantwoordelijk is voor PBG, SLF, opleverdocumenten en herstel bij afwijkingen.",
                ],
            ),
            (
                "Controlepunten",
                [
                    "Vraag welke vergunningen aanwezig zijn, op wiens naam ze staan, voor welk gebouw en welk gebruik ze gelden.",
                    "Vergelijk vergunningen met tekeningen, gebouwd oppervlak, aantal units, toegangsweg, parkeeroplossing, nutsvoorzieningen en feitelijk gebruik.",
                    "Laat een lokale specialist controleren of de vergunningen aansluiten op zoning en exploitatieplan.",
                ],
            ),
        ],
        "faqs": [
            ("Heb ik PBG en SLF nodig bij een villa op Bali?", "Dat hangt af van object, bouwfase en gebruik. Bij aankoop of nieuwbouw horen PBG en SLF in elk geval expliciet in de due diligence te zitten."),
            ("Is een villa zonder volledige vergunningen onverkoopbaar?", "Niet automatisch, maar het vergroot risico. Het kan gevolgen hebben voor prijs, verzekering, verhuur, legalisatie en exit."),
            ("Wie controleert PBG en SLF?", "Laat dit lokaal controleren door een juridisch adviseur, vergunningenspecialist en waar nodig een bouwkundige partij."),
        ],
    },
    {
        "slug": "airbnb-verhuur-bali-vergunningen",
        "title": "Airbnb verhuur Bali vergunningen",
        "h1": "Airbnb verhuur op Bali: vergunningen en risico's",
        "keyword": "Airbnb verhuur Bali vergunningen",
        "description": "Wanneer is Airbnb of short-stay verhuur op Bali juridisch en operationeel risicovol? Lees over zoning, vergunningen, belasting, beheer en realistische netto opbrengst.",
        "short": "Airbnb-verhuur op Bali is niet alleen een rendementsvraag. Je moet controleren of short-stay gebruik past bij zoning, vergunningen, juridische structuur, belastingpositie, beheerafspraken en lokale regels.",
        "sections": [
            (
                "Begin niet bij bezetting, maar bij toegestaan gebruik",
                [
                    "Een hoge verwachte bezettingsgraad zegt weinig als het object niet passend gebruikt mag worden. Controleer eerst of short-stay verhuur bij locatie, zoning en vergunningen past.",
                    "Maak onderscheid tussen eigen gebruik, long-stay verhuur, short-stay verhuur en hospitality-achtige exploitatie. Elk model kan andere verplichtingen geven.",
                ],
            ),
            (
                "Wat je wilt controleren",
                [
                    "Controleer zoning, PBG/SLF, eventuele exploitatievergunningen, belastingregistratie, managementcontract, platformkosten en aansprakelijkheid.",
                    "Vraag wie verantwoordelijk is voor gastenregistratie, schoonmaak, personeel, onderhoud, reviews, klachten, verzekeringen en lokale rapportage.",
                ],
            ),
            (
                "Rendement blijft een scenario",
                [
                    "Bruto omzet uit Airbnb moet worden teruggebracht naar netto resultaat na beheer, OTA-kosten, schoonmaak, onderhoud, personeel, reserveringen, lokale lasten en leegstand.",
                    "Gebruik conservatieve scenario's voor bezetting en dagprijs. Seizoen, concurrentie, locatiekwaliteit en reviews kunnen de opbrengst sterk veranderen.",
                ],
            ),
        ],
        "faqs": [
            ("Kan ik elke villa op Bali via Airbnb verhuren?", "Nee. Dat hangt af van bestemming, vergunningen, juridische structuur, lokale regels en beheerafspraken."),
            ("Wat is het grootste risico bij Airbnb op Bali?", "Dat bruto omzet wordt overschat terwijl vergunningen, kosten, belasting en exploitatieverplichtingen onvoldoende zijn gecontroleerd."),
            ("Is Airbnb-rendement gegarandeerd?", "Nee. Rendement blijft afhankelijk van markt, bezetting, dagprijs, kosten en naleving van regels."),
        ],
    },
    {
        "slug": "beste-gebieden-investeren-bali",
        "title": "Beste gebieden investeren Bali",
        "h1": "Beste gebieden om te investeren in Bali: hoe vergelijk je locaties?",
        "keyword": "beste gebieden investeren Bali",
        "description": "Vergelijk Canggu, Pererenan, Uluwatu, Seminyak, Sanur, Nusa Dua en Tabanan op vraag, risico, prijsniveau, zoning, verhuurpotentie en exit.",
        "short": "Het beste gebied op Bali hangt af van je doel: eigen gebruik, short-stay verhuur, waardegroei of defensieve aankoop. Vergelijk locaties op vraag, prijs, zoning, bereikbaarheid, concurrentie, documentkwaliteit en exit.",
        "sections": [
            (
                "Er bestaat geen universeel beste gebied",
                [
                    "Canggu en Berawa kunnen sterk zijn door vraag en zichtbaarheid, maar kennen ook drukte, concurrentie en hogere prijzen.",
                    "Pererenan, Seseh en Tabanan vragen meer aandacht voor timing, toegang, infrastructuur en toekomstige ontwikkeling.",
                    "Uluwatu, Sanur, Seminyak en Nusa Dua hebben elk een ander vraagprofiel, prijsniveau en type gast of koper.",
                ],
            ),
            (
                "Vergelijk gebieden op harde criteria",
                [
                    "Kijk naar toegang, omgeving, zoning, vergunningen, vraagprofiel, concurrentie, bouwkwaliteit, beheerbaarheid en doorverkoopbaarheid.",
                    "Een populaire locatie is niet automatisch een goede investering als de prijs te hoog is of de juridische basis zwak.",
                ],
            ),
            (
                "Praktische locatiematrix",
                [
                    "Canggu/Berawa: sterke vraag, hoge concurrentie, prijsdruk.",
                    "Pererenan/Seseh: rustiger profiel, groeipotentie, extra aandacht voor omgeving en toegang.",
                    "Uluwatu: premium positionering, schaarste, extra bouwkundige en toegangscontrole.",
                    "Sanur/Nusa Dua: stabieler of premium profiel, ander type doelgroep dan Canggu.",
                ],
            ),
        ],
        "faqs": [
            ("Is Canggu nog interessant voor investeerders?", "Soms wel, maar alleen als prijs, lease, zoning, beheer en exit realistisch zijn. Populariteit alleen is onvoldoende."),
            ("Welke regio is het beste voor short-stay verhuur?", "Dat hangt af van doelgroep, dagprijs, concurrentie, vergunningen en beheerkwaliteit."),
            ("Moet ik kiezen voor een opkomend gebied?", "Alleen als je risico, timing, infrastructuur en exit goed begrijpt. Goedkoop land is niet automatisch investeerbaar."),
        ],
    },
    {
        "slug": "nederlander-investeren-bali-belasting",
        "title": "Nederlander investeren Bali belasting",
        "h1": "Nederlander investeren in Bali: belastingvragen die je vooraf wilt stellen",
        "keyword": "Nederlander investeren Bali belasting",
        "description": "Belastingvragen voor Nederlanders die investeren in Bali vastgoed: Indonesische heffingen, verhuurinkomsten, structuur, Nederland, administratie en fiscale due diligence.",
        "short": "Nederlanders die investeren in Bali moeten belasting niet pas na aankoop bekijken. Indonesische heffingen, verhuurinkomsten, structuur, administratie en Nederlandse fiscale positie kunnen het netto resultaat en risicoprofiel veranderen.",
        "sections": [
            (
                "Belasting hoort bij de aankoopanalyse",
                [
                    "Een rendementsprognose zonder fiscale laag is onvolledig. Lokale heffingen, inkomstenbelasting, bedrijfsstructuur en rapportageverplichtingen kunnen invloed hebben op wat netto overblijft.",
                    "Ook de Nederlandse fiscale positie moet worden bekeken. Buitenlands vermogen, inkomsten en structuur kunnen gevolgen hebben die per persoon verschillen.",
                ],
            ),
            (
                "Welke vragen stel je vooraf?",
                [
                    "Wie ontvangt de huurinkomsten, in welke entiteit of naam, en hoe worden kosten en belastingen verwerkt?",
                    "Welke lokale heffingen, rapportageverplichtingen, bronbelastingen of bedrijfsregistraties kunnen relevant zijn?",
                    "Hoe past de investering in je Nederlandse aangifte en vermogenspositie?",
                ],
            ),
            (
                "Waarom structuur belangrijk is",
                [
                    "Leasehold, Hak Pakai, PT PMA of andere afspraken kunnen fiscale en administratieve gevolgen hebben.",
                    "Laat de fiscale beoordeling aansluiten op juridische structuur, verhuurmodel en exit-scenario. Een fiscaal zwakke structuur kan netto rendement en doorverkoopbaarheid raken.",
                ],
            ),
        ],
        "faqs": [
            ("Betaal ik belasting in Indonesie of Nederland?", "Dat hangt af van structuur, inkomsten, verblijf, bezit en persoonlijke situatie. Laat dit door een fiscalist beoordelen."),
            ("Waarom is belasting belangrijk voor netto rendement?", "Omdat bruto huurinkomsten pas bruikbaar zijn na kosten, beheer, onderhoud, heffingen en rapportageverplichtingen."),
            ("Kan Invest in Bali fiscaal advies geven?", "Nee. De site helpt je betere vragen stellen; fiscale keuzes moeten professioneel worden getoetst."),
        ],
    },
]


def faq_schema(page: dict) -> list[dict]:
    return [
        {
            "@type": "Question",
            "name": question,
            "acceptedAnswer": {"@type": "Answer", "text": answer},
        }
        for question, answer in page["faqs"]
    ]


def priority_head(page: dict) -> str:
    canonical = f"{BASE_URL}/kenniscentrum/{page['slug']}/"
    title = f"{page['title']} | Invest in Bali"
    image = f"{BASE_URL}/assets/gids-2026/due-diligence-zoning.webp"
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": page["h1"],
                "description": page["description"],
                "inLanguage": "nl-NL",
                "dateModified": TODAY,
                "author": {"@type": "Organization", "name": "Invest in Bali", "url": BASE_URL + "/over-ons/"},
                "publisher": {"@type": "Organization", "name": "Invest in Bali", "url": BASE_URL + "/"},
                "mainEntityOfPage": canonical,
                "image": image,
            },
            {"@type": "FAQPage", "mainEntity": faq_schema(page)},
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE_URL + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Kenniscentrum", "item": BASE_URL + "/kenniscentrum/"},
                    {"@type": "ListItem", "position": 3, "name": page["h1"], "item": canonical},
                ],
            },
        ],
    }
    return f"""<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(page['description'])}" />
    <meta name="robots" content="index,follow" />
    <meta name="theme-color" content="#161311" />
    <link rel="canonical" href="{esc(canonical)}" />
    <meta property="og:type" content="article" />
    <meta property="og:locale" content="nl_NL" />
    <meta property="og:site_name" content="Invest in Bali" />
    <meta property="og:title" content="{esc(title)}" />
    <meta property="og:description" content="{esc(page['description'])}" />
    <meta property="og:url" content="{esc(canonical)}" />
    <meta property="og:image" content="{esc(image)}" />
    <meta property="og:image:alt" content="Due diligence documenten, zoningkaart en vastgoedanalyse voor Bali." />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{esc(title)}" />
    <meta name="twitter:description" content="{esc(page['description'])}" />
    <meta name="twitter:image" content="{esc(image)}" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="/styles.css" />
    <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
  </head>"""


def page_html(page: dict) -> str:
    schema_head = priority_head(page)
    faq_items = "\n".join(
        f"""          <details class="faq-item">
            <summary>{esc(question)}</summary>
            <div class="faq-answer"><p>{esc(answer)}</p></div>
          </details>"""
        for question, answer in page["faqs"]
    )
    sections = "\n".join(
        f"""        <article class="content-card">
          <h2>{esc(title)}</h2>
          {"".join(f"<p>{esc(paragraph)}</p>" for paragraph in paragraphs)}
        </article>"""
        for title, paragraphs in page["sections"]
    )
    related = """
        <article class="content-card">
          <h2>Verder lezen</h2>
          <div class="article-list">
            <a class="article-link-card" href="/kenniscentrum/huis-kopen-bali/"><h3>Huis kopen op Bali</h3><p>Lees hoe je locatie, rechten, kosten en doel naast elkaar legt.</p></a>
            <a class="article-link-card" href="/kenniscentrum/leasehold-bali/"><h3>Leasehold Bali</h3><p>Controleer looptijd, verlenging en overdraagbaarheid.</p></a>
            <a class="article-link-card" href="/kenniscentrum/due-diligence-bali/"><h3>Due diligence Bali</h3><p>Welke documenten en aannames wil je voor aankoop toetsen?</p></a>
            <a class="article-link-card" href="/kenniscentrum/rendement-bali-vastgoed/"><h3>Rendement bruto versus netto</h3><p>Reken opbrengst terug naar realistisch netto resultaat.</p></a>
          </div>
        </article>"""
    return f"""<!DOCTYPE html>
<html lang="nl">
  {schema_head}
  <body class="subpage">
    {header()}
    <main>
      <section class="subpage-hero">
        <p class="eyebrow">KENNISCENTRUM</p>
        <h1>{esc(page['h1'])}</h1>
        <p>{esc(page['short'])}</p>
        <p class="form-note">Laatst bijgewerkt: {UPDATED_LABEL}. Geschreven door het Invest in Bali team. Geen juridisch, fiscaal of financieel advies.</p>
      </section>
      <section class="content-shell longform">
        <article class="content-card answer-block">
          <h2>Kort antwoord</h2>
          <p>{esc(page['short'])}</p>
          <p>Laat de uitkomst altijd per concreet object controleren door lokale juridische, fiscale en technische specialisten.</p>
        </article>
{sections}
        <article class="content-card">
          <h2>Veelgestelde vragen</h2>
{faq_items}
        </article>
{related}
        <div class="cta-panel">
          <div>
            <h2>Leg dit naast een concreet object</h2>
            <p>Plan een gesprek om locatie, juridische structuur, vergunningen, rendement, risico's en due diligence samen door te nemen.</p>
          </div>
          <div class="cta-actions">
            <a class="button button-gold" href="/contact/">Plan een call</a>
            <a class="button button-outline" href="/gids/">Download gids</a>
          </div>
        </div>
      </section>
    </main>
    {footer()}
  </body>
</html>
"""


def update_knowledge_index() -> None:
    path = ROOT / "kenniscentrum" / "index.html"
    text = path.read_text(encoding="utf-8")
    block = """
          <article class="content-card knowledge-wide-card">
            <h2>Vragen die kopers echt stellen</h2>
            <p>Hier vind je praktische antwoorden op onderwerpen die vaak terugkomen bij Nederlandse kopers: vergunningen, Airbnb-verhuur, locatiekeuze, belasting en juridische structuur.</p>
            <div class="article-list">
              <a class="article-link-card" href="/kenniscentrum/pbg-slf-bali/"><h3>PBG en SLF op Bali</h3><p>Waarom bouw- en gebruiksdocumenten invloed hebben op risico, verhuur en exit.</p></a>
              <a class="article-link-card" href="/kenniscentrum/airbnb-verhuur-bali-vergunningen/"><h3>Airbnb verhuur en vergunningen</h3><p>Wanneer short-stay verhuur juridisch en operationeel risicovol wordt.</p></a>
              <a class="article-link-card" href="/kenniscentrum/beste-gebieden-investeren-bali/"><h3>Beste gebieden om te investeren</h3><p>Vergelijk Canggu, Pererenan, Uluwatu, Seminyak, Sanur, Nusa Dua en Tabanan.</p></a>
              <a class="article-link-card" href="/kenniscentrum/nederlander-investeren-bali-belasting/"><h3>Nederlander investeren en belasting</h3><p>Welke fiscale vragen je vooraf wilt stellen bij Bali vastgoed.</p></a>
            </div>
          </article>"""
    if "Vragen die kopers echt stellen" not in text:
        text = text.replace("          <article class=\"content-card knowledge-wide-card\">\n            <h2>Verdiepende artikelen voor betere beslissingen</h2>", block + "\n\n          <article class=\"content-card knowledge-wide-card\">\n            <h2>Verdiepende artikelen voor betere beslissingen</h2>", 1)
    path.write_text(text, encoding="utf-8")


def update_llms() -> None:
    llms = ROOT / "llms.txt"
    text = llms.read_text(encoding="utf-8")
    additions = [
        "- PBG en SLF Bali: https://www.investinbali.nl/kenniscentrum/pbg-slf-bali/",
        "- Airbnb verhuur en vergunningen: https://www.investinbali.nl/kenniscentrum/airbnb-verhuur-bali-vergunningen/",
        "- Beste gebieden investeren Bali: https://www.investinbali.nl/kenniscentrum/beste-gebieden-investeren-bali/",
        "- Nederlander investeren en belasting: https://www.investinbali.nl/kenniscentrum/nederlander-investeren-bali-belasting/",
    ]
    marker = "- Vergunningen en certificeringen: https://www.investinbali.nl/kenniscentrum/certificeringen-vergunningen-bali/"
    for item in additions:
        if item not in text:
            text = text.replace(marker, marker + "\n" + item, 1)
    llms.write_text(text, encoding="utf-8")

    full = ROOT / "llms-full.txt"
    full_text = full.read_text(encoding="utf-8")
    extra = """

## Aanvullende kernpagina's

- PBG en SLF op Bali: controleer bouwtoestemming, gebruiksgeschiktheid, opleverdocumenten en aansluiting op zoning.
- Airbnb verhuur op Bali: controleer short-stay gebruik, vergunningen, belasting, beheer, platformkosten en lokale verplichtingen.
- Beste gebieden om te investeren: vergelijk locaties op vraag, prijs, bereikbaarheid, zoning, concurrentie en exit.
- Nederlandse investeerders en belasting: beoordeel Indonesische heffingen, verhuurinkomsten, structuur, administratie en Nederlandse fiscale positie vooraf.
"""
    if "## Aanvullende kernpagina's" not in full_text:
        full_text = full_text.replace("\n## Disclaimer", extra + "\n## Disclaimer")
    full.write_text(full_text, encoding="utf-8")


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    for page in PAGES:
        loc = f"{BASE_URL}/kenniscentrum/{page['slug']}/"
        if loc in text:
            continue
        entry = f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.82</priority>
  </url>
"""
        text = text.replace("</urlset>", entry + "</urlset>")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for page in PAGES:
        target = ROOT / "kenniscentrum" / page["slug"] / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page_html(page), encoding="utf-8")
    update_knowledge_index()
    update_llms()
    update_sitemap()


if __name__ == "__main__":
    main()
    from site_postprocess import enhance_site

    enhance_site()
