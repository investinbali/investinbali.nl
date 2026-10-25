"""Regression checks for source-gated publication and truthful inventory."""

import json
import re
from pathlib import Path

from project_publication import MAX_VISIBLE_PROJECTS, is_public, visible_projects

ROOT = Path(__file__).resolve().parents[1]
projects = json.loads((ROOT / "data/projects.json").read_text(encoding="utf-8"))
eligible = visible_projects(projects)
assert len(eligible) <= MAX_VISIBLE_PROJECTS == 9
assert not is_public({"publicationStatus": "concept"}), "Missing sources must fail closed"
assert not is_public({"publicationStatus": "draft", "publicationSource": {"url": "https://example.com", "checkedOn": "2026-10-25", "scope": "Presentation"}})
assert len(visible_projects([dict(eligible[0], slug=f"example-{i}") for i in range(12)])) == 9

overview = (ROOT / "projecten/index.html").read_text(encoding="utf-8")
cards = re.findall(r'<a class="catalog-card" href="([^"]+)"', overview)
assert cards == [f"/projecten/{project['slug']}/" for project in eligible]
schema = [json.loads(raw) for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', overview, re.S)]
item_list = next(node for item in schema for node in item.get("@graph", []) if node.get("@type") == "ItemList")
assert [item["url"].removeprefix("https://www.investinbali.nl") for item in item_list["itemListElement"]] == cards
sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
home = (ROOT / "index.html").read_text(encoding="utf-8")
script = (ROOT / "script.js").read_text(encoding="utf-8")
for project in projects:
    if is_public(project):
        continue
    url = f"/projecten/{project['slug']}/"
    detail = (ROOT / url.strip("/") / "index.html").read_text(encoding="utf-8")
    assert 'content="noindex,follow"' in detail
    assert "geen actueel vastgoedaanbod" in detail
    assert '"@type": "Product"' not in detail
    assert "Prijs op aanvraag" not in detail
    assert url not in overview and url not in sitemap and url not in home
    assert f'"{project["slug"]}":' not in script

seseh = (ROOT / "projecten/seseh-boutique-villas/index.html").read_text(encoding="utf-8")
assert "https://schema.org/InStock" not in seseh
assert '"@type": "CreativeWork"' in seseh and "geen geverifieerd actueel aanbod" in seseh
about = (ROOT / "over-ons/index.html").read_text(encoding="utf-8")
assert 'id="lokale-verhuurexpertise"' in about
assert 'target="_blank" rel="noopener noreferrer">Bekijk Clarity Homes Bali' in about
for path in ROOT.rglob("*.html"):
    if any(part in {".git", ".vercel", "node_modules", "tmp", "dist", "assets"} for part in path.relative_to(ROOT).parts):
        continue
    markup = path.read_text(encoding="utf-8")
    footer = re.search(r'<footer\b.*?</footer>', markup, re.S)[0]
    assert footer.count('class="footer-rental-link"') == 1, path
    assert 'href="https://clarityhomesbali.com/" target="_blank" rel="noopener noreferrer">Lokale verhuur op Bali — Clarity Homes Bali</a>' in footer, path
print(f"Publication checks passed: {len(eligible)} presentations, max 9, unpublished routes withdrawn, source/schema parity and crawlable footer links.")
