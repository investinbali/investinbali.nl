"""Fast static integrity checks for the generated public site."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

from site_postprocess import PLACEHOLDER_PROJECTS, ROOT, visible_text


def public_html() -> list[Path]:
    result = []
    for path in ROOT.rglob("*.html"):
        parts = path.relative_to(ROOT).parts
        if any(part in {".git", "assets", "node_modules", "seseh-construction-tracker"} for part in parts):
            continue
        result.append(path)
    return result


errors: list[str] = []
pages = public_html()
for path in pages:
    relative = path.relative_to(ROOT).as_posix()
    markup = path.read_text(encoding="utf-8")
    if len(re.findall(r"<h1\b", markup, re.I)) != 1:
        errors.append(f"{relative}: expected one H1")
    if relative != "404.html" and 'rel="canonical"' not in markup:
        errors.append(f"{relative}: missing canonical")
    if '<main id="main-content" tabindex="-1"' not in markup or 'href="#main-content"' not in markup:
        errors.append(f"{relative}: missing skip target/link")
    if re.search(r'<meta\s+name=["\']keywords', markup, re.I):
        errors.append(f"{relative}: meta keywords remains")
    if 'rel="icon"' not in markup:
        errors.append(f"{relative}: missing favicon")
    if "/privacybeleid/" not in markup or "/cookiebeleid/" not in markup:
        errors.append(f"{relative}: missing legal links")
    if "data-cookie-preferences" not in markup:
        errors.append(f"{relative}: missing cookie-preferences control")

    for image in re.findall(r"<img\b[^>]*>", markup, re.I):
        src = re.search(r'\bsrc=["\']([^"\']+)', image, re.I)
        if src and src.group(1).startswith("/assets/") and not ("width=" in image and "height=" in image):
            errors.append(f"{relative}: image lacks dimensions: {src.group(1)}")

    main = re.search(r"<main\b[^>]*>(.*?)</main>", markup, re.I | re.S)
    main_text = visible_text(main.group(1) if main else "")
    for raw in re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', markup, re.I | re.S):
        try:
            schema = json.loads(raw)
        except json.JSONDecodeError as error:
            errors.append(f"{relative}: invalid JSON-LD: {error}")
            continue
        nodes = schema.get("@graph", [schema]) if isinstance(schema, dict) else []
        for node in nodes:
            if isinstance(node, dict) and node.get("@type") == "FAQPage":
                for question in node.get("mainEntity", []):
                    answer = question.get("acceptedAnswer", {}).get("text", "")
                    if visible_text(question.get("name", "")) not in main_text or visible_text(answer) not in main_text:
                        errors.append(f"{relative}: FAQ schema is not visible")

    for href in re.findall(r'href=["\']([^"\']+)', markup, re.I):
        if not href.startswith("/") or href.startswith("//") or href.startswith("/api/"):
            continue
        target_path = urlparse(href).path
        if target_path.startswith("/assets/"):
            target = ROOT / target_path.lstrip("/")
        elif target_path.endswith("/"):
            target = ROOT / target_path.lstrip("/") / "index.html"
        else:
            target = ROOT / target_path.lstrip("/")
        if not target.exists():
            errors.append(f"{relative}: broken internal link {href}")

sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
for slug in PLACEHOLDER_PROJECTS:
    project_markup = (ROOT / "projecten" / slug / "index.html").read_text(encoding="utf-8")
    if 'content="noindex,follow"' not in project_markup:
        errors.append(f"{slug}: placeholder is indexable")
    if '"@type": "Product"' in project_markup:
        errors.append(f"{slug}: placeholder has Product schema")
    if f"/projecten/{slug}/" in sitemap:
        errors.append(f"{slug}: placeholder remains in sitemap")

if errors:
    raise SystemExit("\n".join(errors))
print(f"Verified {len(pages)} public HTML pages with no static integrity errors.")
