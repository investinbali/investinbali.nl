"""Idempotent production safeguards applied after static page generation."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
LOGO = "/assets/logo-variations/villa-gate-variant-01-balanced-door.svg"
PLACEHOLDER_PROJECTS = {
    project["slug"]
    for project in json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
    if project.get("status") == "binnenkort"
}


def visible_text(markup: str) -> str:
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", markup, flags=re.I | re.S)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip().casefold()


def faq_is_visible(node: dict, main_text: str) -> bool:
    for question in node.get("mainEntity", []):
        answer = question.get("acceptedAnswer", {}).get("text", "")
        if visible_text(str(question.get("name", ""))) not in main_text:
            return False
        if visible_text(str(answer)) not in main_text:
            return False
    return bool(node.get("mainEntity"))


def clean_schema(value, main_text: str, placeholder: bool):
    if isinstance(value, list):
        cleaned = [clean_schema(item, main_text, placeholder) for item in value]
        return [item for item in cleaned if item is not None]
    if not isinstance(value, dict):
        return value

    schema_type = value.get("@type")
    types = schema_type if isinstance(schema_type, list) else [schema_type]
    if placeholder and "Product" in types:
        return None
    if "FAQPage" in types and not faq_is_visible(value, main_text):
        return None

    cleaned = {key: clean_schema(item, main_text, placeholder) for key, item in value.items()}
    if "@graph" in cleaned:
        cleaned["@graph"] = [item for item in cleaned["@graph"] if item is not None]
    if "Organization" in types and value.get("@id", "").endswith("#organization"):
        cleaned["logo"] = f"https://www.investinbali.nl{LOGO}"
        cleaned.pop("sameAs", None)
    return cleaned


def enhance_schema(markup: str, main_text: str, placeholder: bool) -> str:
    pattern = re.compile(r'(<script\s+type=["\']application/ld\+json["\']>)(.*?)(</script>)', re.I | re.S)

    def replace(match: re.Match[str]) -> str:
        try:
            data = json.loads(match.group(2))
        except json.JSONDecodeError:
            return match.group(0)
        cleaned = clean_schema(data, main_text, placeholder)
        if cleaned is None or (isinstance(cleaned, dict) and cleaned.get("@graph") == []):
            return ""
        return f'{match.group(1)}{json.dumps(cleaned, ensure_ascii=False)}</script>'

    return pattern.sub(replace, markup)


def add_image_dimensions(markup: str) -> str:
    pattern = re.compile(r"<img\b[^>]*>", re.I)

    def replace(match: re.Match[str]) -> str:
        tag = match.group(0)
        src_match = re.search(r'\bsrc=["\']([^"\']+)["\']', tag, re.I)
        if not src_match or not src_match.group(1).startswith("/assets/"):
            return tag
        asset = ROOT / src_match.group(1).lstrip("/")
        attrs = ""
        if " decoding=" not in tag:
            attrs += ' decoding="async"'
        if " width=" not in tag and " height=" not in tag and asset.exists():
            try:
                with Image.open(asset) as image:
                    width, height = image.size
                attrs += f' width="{width}" height="{height}"'
            except Exception:
                pass
        if not attrs:
            return tag
        return tag[:-2] + attrs + " />" if tag.endswith("/>") else tag[:-1] + attrs + ">"

    return pattern.sub(replace, markup)


def enhance_html(path: Path) -> None:
    markup = path.read_text(encoding="utf-8")
    relative = path.relative_to(ROOT).as_posix()
    project_match = re.fullmatch(r"projecten/([^/]+)/index\.html", relative)
    project_slug = project_match.group(1) if project_match else ""
    placeholder = project_slug in PLACEHOLDER_PROJECTS

    markup = re.sub(r'\s*<meta\s+name=["\']keywords["\'][^>]*>\s*', "\n", markup, flags=re.I | re.S)
    if 'rel="icon"' not in markup:
        markup = markup.replace("</head>", f'    <link rel="icon" href="{LOGO}" type="image/svg+xml" />\n  </head>', 1)
    if 'class="skip-link"' not in markup:
        markup = re.sub(r"(<body\b[^>]*>)", r'\1\n    <a class="skip-link" href="#main-content">Ga naar de inhoud</a>', markup, count=1, flags=re.I)
    markup = re.sub(r"<main(?![^>]*\bid=)", '<main id="main-content" tabindex="-1"', markup, count=1, flags=re.I)

    if relative == "index.html":
        hero_end = markup.find("</section>")
        before, after = markup[:hero_end], markup[hero_end:]
        before = re.sub(r'(<article class="usp-card">.*?<)h3(>.*?</)h3(>)', r'\1h2\2h2\3', before, flags=re.S)
        markup = before + after
        for input_id, attrs in {
            "investment": 'min="1" step="1000"',
            "dailyRate": 'min="0" step="1"',
            "occupancy": 'min="0" max="100" step="1"',
            "costs": 'min="0" max="100" step="1"',
        }.items():
            markup = re.sub(
                rf'(<input\s+id="{input_id}"\s+type="number")(?![^>]*\bmin=)',
                rf'\1 {attrs}',
                markup,
            )

    if placeholder:
        markup = re.sub(r'<meta\s+name="robots"\s+content="[^"]*"\s*/?>', '<meta name="robots" content="noindex,follow" />', markup, count=1)

    main_match = re.search(r"<main\b[^>]*>(.*?)</main>", markup, flags=re.I | re.S)
    main_text = visible_text(main_match.group(1) if main_match else "")
    markup = enhance_schema(markup, main_text, placeholder)
    markup = add_image_dimensions(markup)

    if project_match and project_slug != "seseh-boutique-villas":
        markup = re.sub(r'\s*<p class="illustrative-image-note">.*?</p>', "", markup, flags=re.S)
        markup = re.sub(
            r'(<p class="catalog-location">.*?</p>)',
            r'\1\n          <p class="illustrative-image-note">Illustratieve afbeelding; geen projectspecifieke foto.</p>',
            markup,
            count=1,
            flags=re.S,
        )

    if "/privacybeleid/" not in markup and "<footer" in markup:
        legal = '''
      <div class="footer-column">
        <h4>Privacy</h4>
        <a href="/privacybeleid/">Privacybeleid</a>
        <a href="/cookiebeleid/">Cookiebeleid</a>
      </div>'''
        markup = markup.replace("</footer>", legal + "\n    </footer>", 1)

    footer_match = re.search(r"<footer\b.*?</footer>", markup, flags=re.I | re.S)
    if footer_match and "data-cookie-preferences" not in footer_match.group(0):
        footer = footer_match.group(0)
        footer = footer.replace(
            '<a href="/cookiebeleid/">Cookiebeleid</a>',
            '<a href="/cookiebeleid/">Cookiebeleid</a>\n        <button class="cookie-preferences-link" type="button" data-cookie-preferences>Cookievoorkeuren</button>',
            1,
        )
        markup = markup[: footer_match.start()] + footer + markup[footer_match.end() :]

    markup = re.sub(
        r'<p class="form-success"(?:\s+role="status"\s+aria-live="polite")*',
        '<p class="form-success" role="status" aria-live="polite"',
        markup,
    )
    markup = re.sub(
        r'<p class="form-error"(?:\s+role="alert"\s+aria-live="assertive")*',
        '<p class="form-error" role="alert" aria-live="assertive"',
        markup,
    )
    markup = "\n".join(line.rstrip() for line in markup.splitlines()).rstrip() + "\n"
    path.write_text(markup, encoding="utf-8")


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    markup = path.read_text(encoding="utf-8")
    for slug in PLACEHOLDER_PROJECTS:
        markup = re.sub(
            rf"\s*<url>\s*<loc>https://www\.investinbali\.nl/projecten/{re.escape(slug)}/</loc>.*?</url>",
            "",
            markup,
            flags=re.S,
        )
    for slug in ("privacybeleid", "cookiebeleid"):
        loc = f"https://www.investinbali.nl/{slug}/"
        if loc not in markup:
            entry = f"  <url>\n    <loc>{loc}</loc>\n    <changefreq>yearly</changefreq>\n    <priority>0.3</priority>\n  </url>\n"
            markup = markup.replace("</urlset>", entry + "</urlset>")
    markup = "\n".join(line.rstrip() for line in markup.splitlines()).rstrip() + "\n"
    path.write_text(markup, encoding="utf-8")


def enhance_site() -> None:
    for path in ROOT.rglob("*.html"):
        relative = path.relative_to(ROOT).parts
        if any(part in {".git", "node_modules", "seseh-construction-tracker", "assets"} for part in relative):
            continue
        enhance_html(path)
    update_sitemap()


if __name__ == "__main__":
    enhance_site()
