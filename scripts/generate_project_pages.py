from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.investinbali.nl"

STATUS_LABELS = {
    "te-koop": "Te koop",
    "investering": "Investering",
    "binnenkort": "Binnenkort",
    "uitverkocht": "Uitverkocht",
}

TYPE_LABELS = {
    "villa": "Villa",
    "huis": "Huis",
    "project": "Project",
    "land": "Land",
    "commercial": "Commercial",
}


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def page_head(title: str, description: str, canonical: str, image: str, image_alt: str) -> str:
    image_url = image if image.startswith("http") else f"{BASE_URL}{image}"
    return f"""<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(description)}" />
    <meta name="robots" content="index,follow" />
    <meta name="theme-color" content="#161311" />
    <link rel="canonical" href="{esc(canonical)}" />
    <meta property="og:type" content="website" />
    <meta property="og:locale" content="nl_NL" />
    <meta property="og:site_name" content="Invest in Bali" />
    <meta property="og:title" content="{esc(title)}" />
    <meta property="og:description" content="{esc(description)}" />
    <meta property="og:url" content="{esc(canonical)}" />
    <meta property="og:image" content="{esc(image_url)}" />
    <meta property="og:image:alt" content="{esc(image_alt)}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{esc(title)}" />
    <meta name="twitter:description" content="{esc(description)}" />
    <meta name="twitter:image" content="{esc(image_url)}" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="/styles.css" />
  </head>"""


def header() -> str:
    return """<header class="site-header">
      <a class="brand" href="/" aria-label="Invest in Bali home"><span class="brand-mark">⌂</span><span class="brand-text">INVEST IN BALI</span></a>
      <nav class="main-nav" aria-label="Hoofdnavigatie">
        <a href="/projecten/">Projecten</a>
        <a href="/kenniscentrum/">Kenniscentrum</a>
        <a href="/over-ons/">Over ons</a>
        <a href="/faq/">FAQ</a>
        <a href="/contact/">Contact</a>
      </nav>
      <a class="button button-gold header-cta" href="/contact/">PLAN EEN CALL</a>
    </header>"""


def footer() -> str:
    return """<footer class="site-footer">
      <div>
        <h3>Invest in Bali</h3>
        <p>Projecten op Bali voor kopers en investeerders die duidelijkheid willen over potentie, risico en structuur.</p>
        <a class="footer-email" href="mailto:info@investinbali.nl">info@investinbali.nl</a>
      </div>
      <div class="footer-column">
        <h4>Navigatie</h4>
        <a href="/projecten/">Projecten</a>
        <a href="/kenniscentrum/">Kenniscentrum</a>
        <a href="/faq/">FAQ</a>
        <a href="/contact/">Contact</a>
      </div>
      <div class="footer-column">
        <h4>Populaire zoekvragen</h4>
        <a href="/investeren-in-bali/">Investeren in Bali</a>
        <a href="/huis-kopen-bali/">Huis kopen Bali</a>
        <a href="/villa-kopen-bali/">Villa kopen Bali</a>
        <a href="/vastgoed-bali-rendement/">Bali vastgoed rendement</a>
        <a href="/leasehold-bali/">Leasehold Bali</a>
        <a href="/toekomst-van-bali/">Toekomst van Bali</a>
      </div>
    </footer>
    <script>window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };</script>
    <script defer src="/_vercel/insights/script.js"></script>
    <script src="/analytics-config.js"></script>
    <script src="/script.js"></script>"""


def card(project: dict) -> str:
    status = STATUS_LABELS[project["status"]]
    type_label = TYPE_LABELS[project["type"]]
    slug = project["slug"]
    bedrooms = f"{project.get('bedrooms')} slaapkamers" if project.get("bedrooms") else "Slaapkamers op aanvraag"
    href = f"/projecten/{esc(slug)}/"
    aria = f"Bekijk details van {project['title']}"
    cta = "Bekijk details"
    return f"""<a class="catalog-card" href="{href}" aria-label="{esc(aria)}">
              <div class="catalog-image">
                <img src="{esc(project['thumbnail'])}" alt="{esc(project['title'])} in {esc(project['location'])}" loading="lazy" />
              </div>
              <div class="catalog-body">
                <div class="badge-row">
                  <span class="project-tag">{esc(status)}</span>
                  <span class="project-tag project-tag-soft">{esc(type_label)}</span>
                </div>
                <h3>{esc(project['title'])}</h3>
                <p class="catalog-location">{esc(project['location'])}</p>
                <p class="catalog-description">{esc(project['shortDescription'])}</p>
                <dl class="catalog-facts">
                  <div><dt>Prijs</dt><dd>{esc(project['priceLabel'])}</dd></div>
                  <div><dt>Slaapkamers</dt><dd>{esc(bedrooms)}</dd></div>
                  <div><dt>Structuur</dt><dd>{esc(project['legalStructure'])}</dd></div>
                  <div><dt>Rendement</dt><dd>{esc(project.get('grossYieldLabel', 'Bruto indicatief op aanvraag'))}</dd></div>
                  <div><dt>Doel</dt><dd>{esc(project['investmentGoal'])}</dd></div>
                </dl>
                <span class="button button-outline catalog-cta">{esc(cta)}</span>
              </div>
            </a>"""


def list_items(items: list[str]) -> str:
    return "\n".join(f"<li>{esc(item)}</li>" for item in items)


def fact_rows(project: dict) -> str:
    rows = [
        ("Locatie", project["location"]),
        ("Type woning/project", TYPE_LABELS[project["type"]]),
        ("Status", STATUS_LABELS[project["status"]]),
        ("Prijsindicatie", project["priceLabel"]),
        ("Slaapkamers", project.get("bedrooms", "Op aanvraag")),
        ("Badkamers", project.get("bathrooms", "Op aanvraag")),
        ("Grondoppervlak", project.get("landSize", "Op aanvraag")),
        ("Bouwoppervlak", project.get("buildingSize", "Op aanvraag")),
        ("Juridische structuur", project["legalStructure"]),
        ("Leasehold resterende looptijd", project.get("leaseRemaining", "Te controleren")),
        ("Verlengopties", project.get("extensionOptions", "Te controleren")),
        ("Zoning status", project.get("zoningStatus", "Te controleren op perceelniveau")),
        ("Vergunningenstatus", project.get("permitStatus", "Te controleren")),
        ("Due-diligence status", project.get("dueDiligenceStatus", "Nog niet volledig afgerond")),
        ("Verwachte bruto opbrengst", project.get("grossYieldLabel", "Bruto indicatief op aanvraag")),
        ("Verwachte netto opbrengst", project.get("netYieldLabel", "Afhankelijk van kosten")),
        ("Kostenposten", ", ".join(project.get("costNotes", [])) or "Te controleren"),
        ("Investeringsdoel", project["investmentGoal"]),
        ("Geschikt voor", project["suitableFor"]),
    ]
    return "\n".join(f"<div><dt>{esc(label)}</dt><dd>{esc(value)}</dd></div>" for label, value in rows)


def overview(projects: list[dict]) -> str:
    ordered_projects = sorted(projects, key=lambda project: not project.get("featured", False))
    visible = ordered_projects[:9]
    more_text = (
        '<p class="catalog-note">Meer objecten beschikbaar op aanvraag.</p>'
        if len(projects) > 9
        else ""
    )
    cards = "\n".join(card(project) for project in visible)
    description = "Vergelijk projecten en investeringsobjecten op Bali op locatie, prijs, juridische structuur, risico's en verhuurpotentie."
    return f"""<!DOCTYPE html>
<html lang="nl">
  {page_head("Projecten op Bali | Invest in Bali", description, f"{BASE_URL}/projecten/", "/assets/hero/bali-villa-hero.webp", "Villa op Bali als sfeerbeeld voor vastgoedcatalogus.")}
  <body class="subpage">
    {header()}
    <main>
      <section class="subpage-hero project-hero">
        <p class="eyebrow">VASTGOEDCATALOGUS</p>
        <h1>Projecten op Bali</h1>
        <p>Vergelijk woningen en investeringsprojecten op locatie, prijs, juridische structuur, verhuurpotentie, risico’s en verwachte rendementen.</p>
      </section>
      <section class="content-shell">
        <article class="content-card catalog-intro">
          <h2>Verder kijken dan alleen foto's</h2>
          <p>Deze selectie is bedoeld voor kopers en investeerders die verder willen kijken dan alleen foto’s. Elk object wordt gepresenteerd met vaste informatie, zodat je sneller kunt beoordelen of het past bij jouw doel: aankoop, waardegroei, short-stay verhuur of een combinatie daarvan.</p>
        </article>
        <div class="catalog-grid">
          {cards}
        </div>
        {more_text}
        <div class="catalog-footer">
          <p>Alle informatie is indicatief en afhankelijk van documentcontrole, juridische structuur, vergunningen en marktomstandigheden.</p>
          <a class="text-link" href="/kenniscentrum/">Vergelijk met deze vragen in het kenniscentrum</a>
        </div>
        <div class="cta-panel">
          <div>
            <h2>Wil je een object serieus beoordelen?</h2>
            <p>Plan een gesprek om locatie, structuur, kosten, verhuurpotentie en risico’s door te nemen voordat je verder gaat.</p>
          </div>
          <div class="cta-actions">
            <a class="button button-gold" href="/contact/">Plan een call</a>
            <a class="button button-outline" href="/contact/">Vraag meer info op</a>
          </div>
        </div>
      </section>
    </main>
    {footer()}
  </body>
</html>
"""


def detail(project: dict) -> str:
    status = STATUS_LABELS[project["status"]]
    type_label = TYPE_LABELS[project["type"]]
    description = f"Kritische projectinformatie over {project['title']} in {project['location']}: prijsindicatie, juridische structuur, verhuurpotentie, risico’s en rendementsscenario."
    scenario = project.get("scenario", {})
    external_project_url = project.get("externalProjectUrl")
    external_project_cta = (
        f'\n            <a class="button button-outline" href="{esc(external_project_url)}" target="_blank" rel="noopener noreferrer">Bekijk projectsite</a>'
        if external_project_url
        else ""
    )
    external_walkthrough_url = project.get("externalWalkthroughUrl")
    external_walkthrough_cta = (
        f'\n            <a class="button button-outline" href="{esc(external_walkthrough_url)}" target="_blank" rel="noopener noreferrer">Bekijk 3D walkthrough</a>'
        if external_walkthrough_url
        else ""
    )
    canonical = f"{BASE_URL}/projecten/{project['slug']}/"
    image_url = project["thumbnail"] if project["thumbnail"].startswith("http") else f"{BASE_URL}{project['thumbnail']}"
    product_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": project["title"],
        "description": description,
        "image": image_url,
        "url": canonical,
        "brand": {"@type": "Organization", "name": "Invest in Bali", "url": BASE_URL + "/"},
        "category": f"Bali vastgoed - {type_label}",
        "additionalProperty": [
            {"@type": "PropertyValue", "name": "Locatie", "value": project["location"]},
            {"@type": "PropertyValue", "name": "Juridische structuur", "value": project["legalStructure"]},
            {"@type": "PropertyValue", "name": "Leasehold resterend", "value": project.get("leaseRemaining", "Te controleren")},
            {"@type": "PropertyValue", "name": "Zoning status", "value": project.get("zoningStatus", "Te controleren op perceelniveau")},
            {"@type": "PropertyValue", "name": "Vergunningenstatus", "value": project.get("permitStatus", "Te controleren")},
            {"@type": "PropertyValue", "name": "Due-diligence status", "value": project.get("dueDiligenceStatus", "Nog niet volledig afgerond")},
            {"@type": "PropertyValue", "name": "Bruto rendement indicatief", "value": project.get("grossYieldLabel", "Bruto indicatief op aanvraag")},
            {"@type": "PropertyValue", "name": "Netto scenario", "value": project.get("netYieldLabel", "Afhankelijk van kosten")},
        ],
        "offers": {
            "@type": "Offer",
            "priceCurrency": "EUR",
            "priceSpecification": {"@type": "PriceSpecification", "description": project["priceLabel"]},
            "availability": "https://schema.org/InStock" if project["status"] in ["te-koop", "investering"] else "https://schema.org/PreOrder",
            "url": canonical,
        },
    }
    gallery = "\n".join(
        f'<img src="{esc(src)}" alt="{esc(project["title"])} - afbeelding {index}" loading="lazy" />'
        for index, src in enumerate(project.get("images", []), start=1)
    )
    head = page_head(f"{project['title']} | Investeren in Bali vastgoed", description, canonical, project["thumbnail"], f"{project['title']} in {project['location']}").replace(
        "  </head>",
        f'    <script type="application/ld+json">{json.dumps(product_schema, ensure_ascii=False)}</script>\n  </head>',
    )
    return f"""<!DOCTYPE html>
<html lang="nl">
  {head}
  <body class="subpage">
    {header()}
    <main>
      <section class="project-detail-hero">
        <div class="project-detail-image">
          <img src="{esc(project['thumbnail'])}" alt="{esc(project['title'])} in {esc(project['location'])}" fetchpriority="high" />
        </div>
        <div class="project-detail-copy">
          <div class="badge-row">
            <span class="project-tag">{esc(status)}</span>
            <span class="project-tag project-tag-soft">{esc(type_label)}</span>
          </div>
          <h1>{esc(project['title'])}</h1>
          <p class="catalog-location">{esc(project['location'])}</p>
          <p>{esc(project['shortDescription'])}</p>
          <div class="cta-actions">
            <a class="button button-gold" href="/contact/">Plan een call</a>
            <a class="button button-outline" href="/contact/">Vraag meer info op</a>
            {external_project_cta}
            {external_walkthrough_cta}
            <a class="button button-ghost-dark" href="/projecten/">Terug naar alle projecten</a>
          </div>
        </div>
      </section>
      <section class="content-shell detail-shell">
        <article class="content-card">
          <h2>Kerngegevens</h2>
          <dl class="detail-facts">{fact_rows(project)}</dl>
        </article>
        <div class="grid grid-two">
          <article class="content-card">
            <h2>Waarom dit object interessant kan zijn</h2>
            <ul class="plain-list">{list_items(project['highlights'])}</ul>
          </article>
          <article class="content-card">
            <h2>Waar moet je kritisch naar kijken</h2>
            <ul class="plain-list">
              <li>Juridische structuur</li>
              <li>Zoning / bestemming</li>
              <li>Vergunningen</li>
              <li>Resterende leaseperiode</li>
              <li>Verlengopties</li>
              <li>Beheer- en OTA-kosten</li>
              <li>Bezettingsrisico</li>
              <li>Onderhoud</li>
              <li>Exit / doorverkoopbaarheid</li>
              {list_items(project['risks'])}
            </ul>
          </article>
        </div>
        <article class="content-card scenario-card">
          <h2>Rendementsscenario</h2>
          <dl class="detail-facts scenario-facts">
            <div><dt>Gemiddelde dagprijs</dt><dd>{esc(scenario.get('averageDailyRate', 'Op aanvraag'))}</dd></div>
            <div><dt>Bezettingsgraad</dt><dd>{esc(scenario.get('occupancy', 'Op aanvraag'))}</dd></div>
            <div><dt>Bruto jaaromzet</dt><dd>{esc(scenario.get('grossRevenue', 'Op aanvraag'))}</dd></div>
            <div><dt>Geschatte kosten %</dt><dd>{esc(scenario.get('costPercentage', 'Op aanvraag'))}</dd></div>
            <div><dt>Indicatief netto resultaat</dt><dd>{esc(scenario.get('netResult', 'Op aanvraag'))}</dd></div>
          </dl>
          <p class="form-note">Indicatief scenario. Geen garantie op rendement en geen juridisch of financieel advies.</p>
        </article>
        {f'<article class="content-card"><h2>Afbeeldingen</h2><div class="project-gallery">{gallery}</div></article>' if gallery else ''}
        <div class="cta-panel">
          <div>
            <h2>Wil je dit object serieus beoordelen?</h2>
            <p>Plan een gesprek om locatie, structuur, kosten, verhuurpotentie en risico’s door te nemen voordat je verder gaat.</p>
          </div>
          <div class="cta-actions">
            <a class="button button-gold" href="/contact/">Plan een call</a>
            <a class="button button-outline" href="/contact/">Vraag meer info op</a>
          </div>
        </div>
      </section>
    </main>
    {footer()}
  </body>
</html>
"""


def main() -> None:
    projects = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
    (ROOT / "projecten" / "index.html").write_text(overview(projects), encoding="utf-8")
    for project in projects:
        target = ROOT / "projecten" / project["slug"]
        target.mkdir(parents=True, exist_ok=True)
        (target / "index.html").write_text(detail(project), encoding="utf-8")


if __name__ == "__main__":
    main()
