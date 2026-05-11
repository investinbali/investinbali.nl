from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://www.investinbali.nl"
REPORTS = ROOT / "docs" / "knowledge-base-wiki" / "reports"


ARTICLES = [
    {
        "report": "01-wet-en-regelgeving.md",
        "slug": "wet-en-regelgeving-bali-vastgoed",
        "title": "Wet en regelgeving Bali vastgoed",
        "h1": "Wet en regelgeving voor Bali vastgoed",
        "keyword": "wet en regelgeving Bali vastgoed",
        "description": "Uitleg over wet en regelgeving bij Bali vastgoed: landrechten, zoning, vergunningen, PT PMA, belasting, verhuur en due diligence voor investeerders.",
    },
    {
        "report": "02-continue-updates-wet-regelgeving.md",
        "slug": "wet-regelgeving-updates-bali",
        "title": "Wetgeving Bali vastgoed actueel houden",
        "h1": "Hoe houd je wetgeving rond Bali vastgoed actueel?",
        "keyword": "wetgeving Bali vastgoed updates",
        "description": "Lees waarom regelgeving rond Bali vastgoed actief gemonitord moet worden en welke bronnen belangrijk zijn voor investeerders.",
    },
    {
        "report": "03-bouwnormen.md",
        "slug": "bouwnormen-bali",
        "title": "Bouwnormen Bali vastgoed",
        "h1": "Bouwnormen op Bali: waar moet je op letten?",
        "keyword": "bouwnormen Bali villa",
        "description": "Praktische uitleg over bouwnormen op Bali, PBG, SLF, constructie, drainage, brandveiligheid, MEP en technische due diligence.",
    },
    {
        "report": "04-bouwen-in-bali.md",
        "slug": "bouwen-in-bali",
        "title": "Bouwen in Bali",
        "h1": "Bouwen in Bali: stappen, risico's en controles",
        "keyword": "bouwen in Bali",
        "description": "Overzicht van bouwen in Bali: locatiecheck, zoning, vergunningen, contractorselectie, bouwmanagement, budgetcontrole en oplevering.",
    },
    {
        "report": "05-projectontwikkeling.md",
        "slug": "projectontwikkeling-bali",
        "title": "Projectontwikkeling Bali vastgoed",
        "h1": "Projectontwikkeling op Bali: wanneer is een project investeerbaar?",
        "keyword": "projectontwikkeling Bali vastgoed",
        "description": "Lees hoe je projectontwikkeling op Bali beoordeelt op locatie, juridische structuur, zoning, bouwbaarheid, exploitatie, financiering en exit.",
    },
    {
        "report": "06-land-eigendom-en-overdracht.md",
        "slug": "land-eigendom-overdracht-bali",
        "title": "Land eigendom en overdracht Bali",
        "h1": "Land eigendom en overdracht op Bali",
        "keyword": "land eigendom Bali buitenlander",
        "description": "Uitleg over landrechten, leasehold, Hak Pakai, HGB, overdracht, BPN, PPAT en juridische controle bij vastgoed op Bali.",
    },
    {
        "report": "07-pt-pma-opzetten.md",
        "slug": "pt-pma-opzetten-bali",
        "title": "PT PMA opzetten Bali vastgoed",
        "h1": "PT PMA opzetten voor Bali vastgoed",
        "keyword": "PT PMA opzetten Bali",
        "description": "Wanneer is een PT PMA relevant bij Bali vastgoed, welke rol spelen KBLI, OSS, NIB, kapitaal, administratie, belasting en compliance?",
    },
    {
        "report": "08-boekhouding-bouwprojecten.md",
        "slug": "boekhouding-bouwprojecten-bali",
        "title": "Boekhouding bouwprojecten Bali",
        "h1": "Boekhouding voor bouwprojecten op Bali",
        "keyword": "boekhouding bouwproject Bali",
        "description": "Waarom bouwprojecten op Bali budgetcontrole, facturen, betalingsbewijzen, change orders, taxes, reserves en rapportage nodig hebben.",
    },
    {
        "report": "09-project-management.md",
        "slug": "project-management-bali-vastgoed",
        "title": "Project management Bali vastgoed",
        "h1": "Project management voor Bali vastgoed",
        "keyword": "project management Bali vastgoed",
        "description": "Projectmanagement voor Bali vastgoed: planning, RACI, budget tracker, risk register, decision log, change orders en voortgangsrapportage.",
    },
    {
        "report": "10-buitenlandse-investeerders.md",
        "slug": "buitenlandse-investeerders-bali-vastgoed",
        "title": "Buitenlandse investeerders Bali vastgoed",
        "h1": "Buitenlandse investeerders in Bali vastgoed",
        "keyword": "buitenlandse investeerders Bali vastgoed",
        "description": "Wat buitenlandse investeerders moeten beoordelen bij Bali vastgoed: rechten, structuur, risico's, rendement, rapportage, kosten en exit.",
    },
    {
        "report": "11-juridische-hulp-indonesie.md",
        "slug": "juridische-hulp-indonesie-vastgoed",
        "title": "Juridische hulp Indonesië vastgoed",
        "h1": "Juridische hulp in Indonesië bij vastgoed",
        "keyword": "juridische hulp Indonesië vastgoed",
        "description": "Welke juridische hulp heb je nodig bij vastgoed in Indonesië: advocaat, notaris, PPAT, fiscalist en vergunningenspecialist.",
    },
    {
        "report": "12-certificeringen-en-vergunningen.md",
        "slug": "certificeringen-vergunningen-bali",
        "title": "Certificeringen en vergunningen Bali",
        "h1": "Certificeringen en vergunningen voor Bali vastgoed",
        "keyword": "vergunningen Bali vastgoed",
        "description": "Overzicht van vergunningen en certificeringen voor Bali vastgoed: OSS, NIB, KBLI, zoning, PBG, SLF en tourism licensing.",
    },
    {
        "report": "13-verzekeringen.md",
        "slug": "verzekeringen-bali-vastgoed",
        "title": "Verzekeringen Bali vastgoed",
        "h1": "Verzekeringen voor Bali vastgoed",
        "keyword": "verzekering Bali vastgoed",
        "description": "Welke verzekeringen relevant kunnen zijn voor Bali vastgoed: bouw, eigendom, verhuur, aansprakelijkheid, natuurrisico's en personeel.",
    },
    {
        "report": "14-verhuur.md",
        "slug": "verhuur-bali-villa",
        "title": "Villa verhuur Bali",
        "h1": "Villa verhuur op Bali: short-stay, vergunningen en risico's",
        "keyword": "villa verhuur Bali",
        "description": "Villa verhuur op Bali uitgelegd: short-stay, long-stay, villa management, KBLI, NIB, zoning, belasting, platformkosten en compliance.",
    },
    {
        "report": "15-personeel-aannemen.md",
        "slug": "personeel-aannemen-bali",
        "title": "Personeel aannemen Bali villa",
        "h1": "Personeel aannemen voor een villa op Bali",
        "keyword": "personeel aannemen Bali villa",
        "description": "Wat je moet weten over personeel aannemen op Bali: contracten, payroll, BPJS, THR, belasting, werkgeversrol en villa-exploitatie.",
    },
    {
        "report": "16-rechten-plichten.md",
        "slug": "rechten-plichten-bali-vastgoed",
        "title": "Rechten en plichten Bali vastgoed",
        "h1": "Rechten en plichten bij Bali vastgoed",
        "keyword": "rechten plichten Bali vastgoed",
        "description": "Uitleg over rechten en plichten bij Bali vastgoed voor koper, investeerder, leaseholder, developer, operator, werknemer en contractor.",
    },
]


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def slug_to_path(slug: str) -> Path:
    return ROOT / "kenniscentrum" / slug / "index.html"


def section(text: str, heading: str) -> str:
    pattern = rf"## {re.escape(heading)}\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, flags=re.S)
    return match.group(1).strip() if match else ""


def first_paragraph(text: str) -> str:
    for block in re.split(r"\n\s*\n", text.strip()):
        block = block.strip()
        if block and not block.startswith(("-", "#", "Status:", "Laatste", "Eigenaar:", "Risico:")):
            return block
    return ""


def bullets(text: str, max_items: int = 8) -> list[str]:
    found = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("- "):
            found.append(line[2:].strip())
    return found[:max_items]


def sources(text: str, max_items: int = 6) -> list[tuple[str, str]]:
    block = section(text, "Bronnen")
    items = []
    for line in block.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        body = line[2:]
        url_match = re.search(r"https?://\S+", body)
        if not url_match:
            continue
        url = url_match.group(0).rstrip(").,")
        label = body[: url_match.start()].strip(" :-")
        items.append((label or url, url))
    return items[:max_items]


def md_inline(text: str) -> str:
    text = public_text(text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    return esc(text)


def public_text(text: str) -> str:
    replacements = {
        "Voor Invest in Bali betekent dit": "Voor kopers en investeerders betekent dit",
        "Voor Invest in Bali is": "Voor kopers en investeerders is",
        "Voor Invest in Bali zijn": "Voor kopers en investeerders zijn",
        "Voor Invest in Bali": "Voor kopers en investeerders",
        "Invest in Bali betekent dit": "Voor kopers en investeerders betekent dit",
        "De knowledge base moet drie doelen dienen.": "Een goede kennisbasis heeft drie doelen.",
        "knowledge base": "kennisbasis",
        "Knowledge base": "Kennisbasis",
        "de wiki moet niet vervangen": "publieke informatie vervangt niet",
        "De wiki moet niet vervangen": "Publieke informatie vervangt niet",
        "wiki": "kennisbasis",
        "Wiki": "Kennisbasis",
        "sales en marketing beschermen tegen te stellige claims": "voorkomen dat verkoopinformatie te stellig wordt",
        "salesclaims": "verkoopclaims",
        "Salesclaims": "Verkoopclaims",
        "salesmateriaal": "publieke informatie",
        "Salesmateriaal": "Publieke informatie",
        "intern verkeerde aannames": "verkeerde aannames",
        "intern": "in de beoordeling",
        "Intern": "In de beoordeling",
        "database": "kennisbasis",
        "Database": "Kennisbasis",
        "Invest in Bali moet": "Een project moet",
        "Invest in Bali beoordeelt": "Een zorgvuldige beoordeling bekijkt",
        "het bedrijf per project": "je per project",
        "Het bedrijf per project": "Je per project",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def paragraphs_from(text: str, max_paragraphs: int = 3) -> str:
    parts = []
    for block in re.split(r"\n\s*\n", text.strip()):
        block = block.strip()
        if not block or block.startswith("#") or block.startswith("- "):
            continue
        if block.startswith(("Status:", "Laatste", "Eigenaar:", "Risico:")):
            continue
        parts.append(f"<p>{md_inline(block)}</p>")
        if len(parts) >= max_paragraphs:
            break
    return "\n".join(parts)


def page_head(article: dict) -> str:
    canonical = f"{BASE_URL}/kenniscentrum/{article['slug']}/"
    title = f"{article['title']} | Invest in Bali"
    image = f"{BASE_URL}/assets/gids-2026/due-diligence-zoning.webp"
    faq = [
        {
            "question": f"Waarom is {article['keyword']} belangrijk?",
            "answer": f"{article['keyword']} bepaalt welke controles nodig zijn voordat een koper of investeerder een object op Bali serieus beoordeelt.",
        },
        {
            "question": "Is dit juridisch of financieel advies?",
            "answer": "Nee. De informatie is praktische oriëntatie. Laat documenten, vergunningen, fiscale positie en juridische structuur altijd lokaal controleren.",
        },
    ]
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": article["h1"],
                "description": article["description"],
                "inLanguage": "nl-NL",
                "dateModified": "2026-05-11",
                "author": {"@type": "Organization", "name": "Invest in Bali"},
                "publisher": {"@type": "Organization", "name": "Invest in Bali"},
                "mainEntityOfPage": canonical,
                "image": image,
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": item["question"],
                        "acceptedAnswer": {"@type": "Answer", "text": item["answer"]},
                    }
                    for item in faq
                ],
            },
        ],
    }
    return f"""<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(article['description'])}" />
    <meta name="robots" content="index,follow" />
    <meta name="theme-color" content="#161311" />
    <link rel="canonical" href="{esc(canonical)}" />
    <meta property="og:type" content="article" />
    <meta property="og:locale" content="nl_NL" />
    <meta property="og:site_name" content="Invest in Bali" />
    <meta property="og:title" content="{esc(title)}" />
    <meta property="og:description" content="{esc(article['description'])}" />
    <meta property="og:url" content="{esc(canonical)}" />
    <meta property="og:image" content="{esc(image)}" />
    <meta property="og:image:alt" content="Due diligence documenten, zoningkaart en vastgoedanalyse voor Bali." />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{esc(title)}" />
    <meta name="twitter:description" content="{esc(article['description'])}" />
    <meta name="twitter:image" content="{esc(image)}" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="/styles.css" />
    <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
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
      <a class="button button-gold header-cta" href="/gids/">DOWNLOAD GIDS</a>
    </header>"""


def footer() -> str:
    return """<footer class="site-footer">
      <div>
        <h3>Invest in Bali</h3>
        <p>Huizen op Bali voor kopers en investeerders die duidelijkheid willen over potentie, risico en structuur.</p>
      </div>
      <div class="footer-links">
        <a href="/projecten/">Projecten</a>
        <a href="/kenniscentrum/">Kenniscentrum</a>
        <a href="/faq/">FAQ</a>
        <a href="/contact/">Contact</a>
      </div>
    </footer>
    <script src="/script.js"></script>"""


def article_page(article: dict) -> str:
    report = (REPORTS / article["report"]).read_text(encoding="utf-8")
    summary = section(report, "Managementsamenvatting")
    relevance = section(report, "Relevantie voor Invest in Bali")
    checklist = bullets(section(report, "Due diligence checklist") or report, 8)
    red_flags = bullets(section(report, "Rode vlaggen"), 8)
    source_items = sources(report)
    checklist_html = "\n".join(f"<li>{md_inline(item)}</li>" for item in checklist)
    red_flags_html = "\n".join(f"<li>{md_inline(item)}</li>" for item in red_flags)
    source_html = "\n".join(
        f'<li><a href="{esc(url)}">{md_inline(label)}</a></li>' for label, url in source_items
    )
    intro = first_paragraph(summary) or article["description"]
    return f"""<!DOCTYPE html>
<html lang="nl">
  {page_head(article)}
  <body class="subpage">
    {header()}
    <main>
      <section class="subpage-hero">
        <p class="eyebrow">KENNISCENTRUM</p>
        <h1>{esc(article['h1'])}</h1>
        <p>{md_inline(intro)}</p>
        <p class="form-note">Laatst gecontroleerd: 11 mei 2026. Praktische oriëntatie, geen juridisch, fiscaal of financieel advies.</p>
      </section>
      <section class="content-shell longform">
        <article class="content-card">
          <h2>Waarom dit belangrijk is</h2>
          {paragraphs_from(summary, 3)}
        </article>
        <article class="content-card">
          <h2>Wat je moet controleren</h2>
          {paragraphs_from(relevance, 2)}
          <ul class="plain-list">{checklist_html}</ul>
        </article>
        <article class="content-card">
          <h2>Rode vlaggen</h2>
          <p>Gebruik deze punten als eerste filter. Een rode vlag betekent niet automatisch dat een object onmogelijk is, maar wel dat documentcontrole en lokale review nodig zijn.</p>
          <ul class="plain-list">{red_flags_html}</ul>
        </article>
        <article class="content-card">
          <h2>Praktische aanpak</h2>
          <p>Begin met het doel van de aankoop: eigen gebruik, waardegroei, short-stay verhuur of projectontwikkeling. Koppel daarna elke aanname aan documenten, vergunningen, lokale regels en een realistisch kostenmodel.</p>
          <p>Bij Bali vastgoed is vooral belangrijk dat verkoopinformatie, juridische structuur en exploitatiepotentie niet los van elkaar worden beoordeeld. Een aantrekkelijke locatie is pas interessant wanneer rechten, gebruik, kosten en exit ook verdedigbaar zijn.</p>
        </article>
        <article class="content-card">
          <h2>Bronnen en verdere controle</h2>
          <p>Gebruik primaire bronnen waar mogelijk. Commerciële marktinformatie kan nuttig zijn als context, maar mag geen vervanging zijn voor documentcontrole of lokale juridische beoordeling.</p>
          <ul class="source-list">{source_html}</ul>
        </article>
        <div class="cta-panel">
          <div>
            <h2>Wil je dit toepassen op een concreet object?</h2>
            <p>Plan een gesprek of vraag meer informatie op. Dan beoordelen we locatie, structuur, kosten, verhuurpotentie en risico's aan de hand van jouw situatie.</p>
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


def article_cards() -> str:
    return "\n".join(
        f'''              <a class="article-link-card" href="/kenniscentrum/{esc(article['slug'])}/">
                <h3>{esc(article['h1'])}</h3>
                <p>{esc(article['description'])}</p>
              </a>'''
        for article in ARTICLES
    )


def replace_article_lists() -> None:
    for relative in ["kenniscentrum/wiki/index.html"]:
        path = ROOT / relative
        text = path.read_text(encoding="utf-8")
        text = re.sub(
            r'<div class="article-list">.*?</div>\s*</article>',
            f'<div class="article-list">\n{article_cards()}\n            </div>\n          </article>',
            text,
            count=1,
            flags=re.S,
        )
        path.write_text(text, encoding="utf-8")

    index_path = ROOT / "kenniscentrum" / "index.html"
    text = index_path.read_text(encoding="utf-8")
    insert = f"""
          <article class="content-card">
            <h2>Uitgebreide SEO-artikelen</h2>
            <p>Deze verdiepende artikelen beantwoorden concrete vragen over Bali vastgoed, regelgeving, bouwen, verhuur, projectontwikkeling en investeerdersrisico's.</p>
            <div class="article-list">
{article_cards()}
            </div>
          </article>"""
    if "Uitgebreide SEO-artikelen" not in text:
        text = text.replace("</div>\n      </section>\n    </main>", f"{insert}\n        </div>\n      </section>\n    </main>", 1)
    index_path.write_text(text, encoding="utf-8")


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    for article in ARTICLES:
        loc = f"{BASE_URL}/kenniscentrum/{article['slug']}/"
        if loc in text:
            continue
        entry = f"""  <url>
    <loc>{loc}</loc>
    <lastmod>2026-05-11</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.75</priority>
  </url>
"""
        text = text.replace("</urlset>", entry + "</urlset>")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for article in ARTICLES:
        target = slug_to_path(article["slug"])
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(article_page(article), encoding="utf-8")
    replace_article_lists()
    update_sitemap()


if __name__ == "__main__":
    main()
