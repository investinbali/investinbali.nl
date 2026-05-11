from __future__ import annotations

import hashlib
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.tableofcontents import TableOfContents


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "content" / "gids-investeren-in-bali-2026.md"
OUT = ROOT / "dist" / "gratis-gids-investeren-in-bali-2026.pdf"
ASSETS = ROOT / "assets" / "gids-2026"

URLS = {
    "Plan een call": "https://www.investinbali.nl/contact/",
    "Download gids": "https://www.investinbali.nl/gids/",
    "Bekijk huizen": "https://www.investinbali.nl/projecten/",
}

PAGE_W, PAGE_H = A4

INK = colors.HexColor("#17221f")
MUTED = colors.HexColor("#5f6b66")
GOLD = colors.HexColor("#b88a3d")
GOLD_DARK = colors.HexColor("#8b6426")
GREEN = colors.HexColor("#21483f")
LIGHT = colors.HexColor("#f7f3ec")
LINE = colors.HexColor("#ddd2c0")
WHITE = colors.white


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("EUR", "€")
    )


def make_styles():
    base = getSampleStyleSheet()
    styles = {}
    styles["Title"] = ParagraphStyle(
        "GuideTitle",
        parent=base["Title"],
        fontName="Times-Bold",
        fontSize=34,
        leading=38,
        textColor=WHITE,
        alignment=TA_LEFT,
        spaceAfter=10,
    )
    styles["CoverSub"] = ParagraphStyle(
        "CoverSub",
        parent=base["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=18,
        textColor=colors.HexColor("#f5efe2"),
        alignment=TA_LEFT,
    )
    styles["Eyebrow"] = ParagraphStyle(
        "Eyebrow",
        parent=base["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=GOLD,
        uppercase=True,
        spaceAfter=8,
    )
    styles["H1"] = ParagraphStyle(
        "ChapterHeading",
        parent=base["Heading1"],
        fontName="Times-Bold",
        fontSize=22,
        leading=27,
        textColor=GREEN,
        spaceBefore=12,
        spaceAfter=10,
        keepWithNext=True,
    )
    styles["H2"] = ParagraphStyle(
        "SectionHeading",
        parent=base["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=INK,
        spaceBefore=9,
        spaceAfter=5,
        keepWithNext=True,
    )
    styles["Body"] = ParagraphStyle(
        "GuideBody",
        parent=base["BodyText"],
        fontName="Helvetica",
        fontSize=9.6,
        leading=14.3,
        textColor=INK,
        spaceAfter=7,
    )
    styles["Small"] = ParagraphStyle(
        "Small",
        parent=styles["Body"],
        fontSize=8,
        leading=11,
        textColor=MUTED,
    )
    styles["Bullet"] = ParagraphStyle(
        "Bullet",
        parent=styles["Body"],
        leftIndent=17,
        firstLineIndent=0,
        bulletIndent=4,
        bulletFontName="Helvetica",
        bulletFontSize=8.5,
        spaceAfter=4,
    )
    styles["Pull"] = ParagraphStyle(
        "Pull",
        parent=styles["Body"],
        fontName="Times-Bold",
        fontSize=16,
        leading=21,
        textColor=GREEN,
        alignment=TA_LEFT,
        spaceAfter=0,
    )
    styles["TocTitle"] = ParagraphStyle(
        "TocTitle",
        parent=styles["H1"],
        fontSize=26,
        leading=31,
        spaceAfter=14,
    )
    styles["CTA"] = ParagraphStyle(
        "CTA",
        parent=styles["Body"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=WHITE,
        alignment=TA_CENTER,
    )
    return styles


class CoverPage(Flowable):
    def __init__(self, image_path: Path, styles):
        super().__init__()
        self.image_path = str(image_path)
        self.styles = styles

    def wrap(self, avail_width, avail_height):
        return PAGE_W, PAGE_H

    def draw(self):
        c = self.canv
        c.saveState()
        c.drawImage(self.image_path, 0, 0, PAGE_W, PAGE_H, preserveAspectRatio=True, anchor="c")
        c.setFillColor(colors.Color(0, 0, 0, alpha=0.47))
        c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        c.setFillColor(colors.Color(0.07, 0.12, 0.10, alpha=0.62))
        c.rect(0, 0, PAGE_W, 8.8 * cm, stroke=0, fill=1)
        c.setFillColor(GOLD)
        c.rect(0, 8.8 * cm, PAGE_W, 2.3 * mm, stroke=0, fill=1)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(2.1 * cm, PAGE_H - 2.1 * cm, "INVEST IN BALI")
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(GOLD)
        c.drawString(2.1 * cm, 7.75 * cm, "GRATIS GIDS 2026")
        text = c.beginText(2.1 * cm, 6.85 * cm)
        text.setFont("Times-Bold", 32)
        text.setFillColor(WHITE)
        for line in ["Investeren", "in Bali"]:
            text.textLine(line)
        c.drawText(text)
        c.setFillColor(colors.HexColor("#f5efe2"))
        c.setFont("Helvetica", 11)
        sub = "Huizen kopen met helder zicht op rendement, risico, leasehold en zoning."
        self._draw_wrapped(c, sub, 2.1 * cm, 3.35 * cm, PAGE_W - 4.2 * cm, 15)
        c.setFont("Helvetica-Bold", 8.5)
        c.setFillColor(GOLD)
        c.drawString(2.1 * cm, 2.1 * cm, "Voor Nederlandstalige investeerders")
        c.restoreState()

    @staticmethod
    def _draw_wrapped(c, text, x, y, width, leading):
        words = text.split()
        line = ""
        lines = []
        for word in words:
            test = (line + " " + word).strip()
            if stringWidth(test, "Helvetica", 11) <= width:
                line = test
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
        for index, line in enumerate(lines):
            c.drawString(x, y - index * leading, line)


class HeroImage(Flowable):
    def __init__(self, image_path: Path, caption: str, width: float, ratio: float = 0.36):
        super().__init__()
        self.image_path = str(image_path)
        self.caption = caption
        self.width = width
        self.height = width * ratio

    def wrap(self, avail_width, avail_height):
        return self.width, self.height + 18

    def draw(self):
        c = self.canv
        c.saveState()
        c.drawImage(self.image_path, 0, 18, self.width, self.height, preserveAspectRatio=True, anchor="c")
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 7.5)
        c.drawString(0, 5, self.caption)
        c.restoreState()


class Box(Flowable):
    def __init__(self, flowables, fill=LIGHT, stroke=LINE, pad=10):
        super().__init__()
        self.flowables = flowables
        self.fill = fill
        self.stroke = stroke
        self.pad = pad
        self.width = 0
        self.height = 0

    def wrap(self, avail_width, avail_height):
        self.width = avail_width
        inner_w = avail_width - 2 * self.pad
        height = self.pad
        for flowable in self.flowables:
            _, h = flowable.wrap(inner_w, avail_height)
            height += h
        height += self.pad
        self.height = height
        return avail_width, height

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(self.fill)
        c.setStrokeColor(self.stroke)
        c.roundRect(0, 0, self.width, self.height, 4, stroke=1, fill=1)
        y = self.height - self.pad
        inner_w = self.width - 2 * self.pad
        for flowable in self.flowables:
            _, h = flowable.wrap(inner_w, y)
            y -= h
            flowable.drawOn(c, self.pad, y)
        c.restoreState()


class LinkButton(Flowable):
    def __init__(self, label: str, url: str, width: float = 5.3 * cm, height: float = 0.88 * cm):
        super().__init__()
        self.label = label
        self.url = url
        self.width = width
        self.height = height

    def wrap(self, avail_width, avail_height):
        return self.width, self.height + 6

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(GOLD)
        c.setStrokeColor(GOLD_DARK)
        c.roundRect(0, 6, self.width, self.height, 3, stroke=1, fill=1)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(self.width / 2, 6 + self.height / 2 - 3.5, self.label)
        c.linkURL(self.url, (0, 6, self.width, 6 + self.height), relative=1, thickness=0)
        c.restoreState()


class GuideDoc(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, pagesize=A4, **kwargs)
        frame = Frame(
            2.05 * cm,
            1.85 * cm,
            PAGE_W - 4.1 * cm,
            PAGE_H - 3.9 * cm,
            id="normal",
            showBoundary=0,
        )
        cover = Frame(
            0,
            0,
            PAGE_W,
            PAGE_H,
            id="cover",
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            showBoundary=0,
        )
        self.addPageTemplates(
            [
                PageTemplate(id="Cover", frames=[cover], onPage=self.draw_cover_page),
                PageTemplate(id="Normal", frames=[frame], onPage=self.draw_page),
            ]
        )

    def draw_cover_page(self, canvas, doc):
        pass

    def draw_page(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(INK)
        canvas.setFont("Helvetica-Bold", 7.5)
        canvas.drawString(2.05 * cm, PAGE_H - 1.05 * cm, "INVEST IN BALI")
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawRightString(PAGE_W - 2.05 * cm, PAGE_H - 1.05 * cm, "Gratis gids investeren in Bali 2026")
        canvas.setStrokeColor(LINE)
        canvas.line(2.05 * cm, PAGE_H - 1.25 * cm, PAGE_W - 2.05 * cm, PAGE_H - 1.25 * cm)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 8)
        canvas.drawCentredString(PAGE_W / 2, 1.05 * cm, str(canvas.getPageNumber() - 1))
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            style_name = flowable.style.name
            if style_name == "ChapterHeading":
                text = flowable.getPlainText()
                key = safe_key("h1", text, self.page)
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(text, key, level=0, closed=False)
                self.notify("TOCEntry", (0, text, self.page - 1, key))
            elif style_name == "SectionHeading":
                text = flowable.getPlainText()
                key = safe_key("h2", text, self.page)
                self.canv.bookmarkPage(key)
                self.notify("TOCEntry", (1, text, self.page - 1, key))


def safe_key(prefix: str, text: str, page: int) -> str:
    digest = hashlib.sha1(f"{page}:{text}".encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{page}_{digest}"


def parse_markdown(md: str, styles):
    lines = md.splitlines()
    story = []
    para = []
    bullets = []
    skip_toc = False
    in_sources = False

    def flush_para():
        nonlocal para
        if para:
            text = " ".join(para).strip()
            if text.startswith("CTA:"):
                text = text.replace("CTA:", "").strip()
                story.append(cta_button(text, styles))
            else:
                story.append(Paragraph(esc(text), styles["Body"]))
            para = []

    def flush_bullets():
        nonlocal bullets
        if bullets:
            for item in bullets:
                story.append(Paragraph(esc(item), styles["Bullet"], bulletText="•"))
            story.append(Spacer(1, 3))
            bullets = []

    for raw in lines:
        line = raw.rstrip()
        if line.startswith("## Inhoud"):
            skip_toc = True
            continue
        if skip_toc:
            if line.startswith("## "):
                skip_toc = False
            else:
                continue

        if not line.strip():
            flush_para()
            flush_bullets()
            continue

        if line.startswith("# "):
            continue

        if line.startswith("## "):
            flush_para()
            flush_bullets()
            title = line[3:].strip()
            if title == "Bronnen en toetsingskader":
                in_sources = True
            hero = None
            if title.startswith("5. Zoning"):
                hero = HeroImage(ASSETS / "due-diligence-zoning.png", "Zoning en due diligence horen bij de eerste beoordeling, niet bij de afronding.", 16.0 * cm)
            if title.startswith("7. Rendement"):
                hero = HeroImage(ASSETS / "rendement-short-stay.png", "Rendement wordt pas bruikbaar wanneer kosten, bezetting en beheer zijn meegenomen.", 16.0 * cm)
            heading = Paragraph(esc(title), styles["H1"])
            if hero:
                story.append(KeepTogether([heading, hero, Spacer(1, 8)]))
            else:
                story.append(heading)
            continue

        if line.startswith("### "):
            flush_para()
            flush_bullets()
            story.append(Paragraph(esc(line[4:].strip()), styles["H2"]))
            continue

        if line.startswith("- "):
            flush_para()
            bullet = line[2:].strip()
            bullets.append(bullet)
            continue

        if re.match(r"^\d+\.\s+", line):
            flush_para()
            bullets.append(re.sub(r"^\d+\.\s+", "", line).strip())
            continue

        if in_sources and line.startswith("http"):
            story.append(Paragraph(esc(line), styles["Small"]))
            continue

        para.append(line.strip())

    flush_para()
    flush_bullets()
    return story


def cta_button(label: str, styles):
    return LinkButton(label, URLS.get(label, "https://www.investinbali.nl/"))


def build_story(styles):
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            name="TOCHeading1",
            fontName="Helvetica-Bold",
            fontSize=9.6,
            leading=13,
            leftIndent=0,
            firstLineIndent=0,
            spaceBefore=5,
            textColor=INK,
        ),
        ParagraphStyle(
            name="TOCHeading2",
            fontName="Helvetica",
            fontSize=8.2,
            leading=11,
            leftIndent=11,
            firstLineIndent=0,
            textColor=MUTED,
        ),
    ]

    intro_box = Box(
        [
            Paragraph("Waar deze gids voor bedoeld is", styles["H2"]),
            Paragraph(
                "Gebruik deze gids als eerste filter voordat je een woning op Bali serieus onderzoekt. "
                "De inhoud helpt je gerichter vragen te stellen over locatie, leasehold, zoning, due diligence, "
                "kosten en realistische verhuurpotentie.",
                styles["Body"],
            ),
        ]
    )

    disclaimer_box = Box(
        [
            Paragraph("Disclaimer en semi-juridische noot", styles["H2"]),
            Paragraph(
                "Deze gids is algemene informatie en geen juridisch, fiscaal, financieel of beleggingsadvies. "
                "Indonesische regelgeving, lokale vergunningen, zoning en fiscale behandeling kunnen per object "
                "en situatie verschillen. Laat een concrete aankoop altijd controleren door een onafhankelijke "
                "lokale jurist, notaris/PPAT, fiscalist en waar nodig een bouwkundig adviseur.",
                styles["Small"],
            ),
        ],
        fill=colors.HexColor("#fff8ea"),
        stroke=GOLD,
    )

    story = [
        CoverPage(ASSETS / "cover-villa.png", styles),
        NextPageTemplate("Normal"),
        PageBreak(),
        Paragraph("Inhoudsopgave", styles["TocTitle"]),
        Paragraph(
            "Een praktische route door de belangrijkste vragen rond huizen kopen op Bali, leasehold, PT PMA, zoning, rendement en risico.",
            styles["Body"],
        ),
        Spacer(1, 8),
        toc,
        PageBreak(),
        intro_box,
        Spacer(1, 10),
        disclaimer_box,
        Spacer(1, 12),
    ]

    story.extend(parse_markdown(SOURCE.read_text(encoding="utf-8"), styles))

    story.extend(
        [
            PageBreak(),
            Box(
                [
                    Paragraph("Volgende stap", styles["H1"]),
                    Paragraph(
                        "Wil je een woning of zoekprofiel concreet beoordelen? Gebruik de gids als eerste filter en bespreek daarna je doel, budget, voorkeursgebieden en risicoprofiel.",
                        styles["Body"],
                    ),
                    Paragraph("Plan een call", styles["H2"]),
                    Paragraph("Bespreek je situatie, budget en investeringsdoel in een vrijblijvend gesprek.", styles["Body"]),
                    cta_button("Plan een call", styles),
                    Paragraph("Vraag meer info op", styles["H2"]),
                    Paragraph("Ontvang updates over nieuwe huizen, marktinzichten en relevante ontwikkelingen.", styles["Body"]),
                    cta_button("Vraag meer info op", styles),
                    Paragraph("Bekijk huizen", styles["H2"]),
                    Paragraph("Vergelijk woningen op locatie, profiel, potentie en aandachtspunten.", styles["Body"]),
                    cta_button("Bekijk huizen", styles),
                ],
                fill=colors.HexColor("#eef3ef"),
                stroke=colors.HexColor("#bdd0c5"),
                pad=13,
            )
        ]
    )
    return story


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    styles = make_styles()
    doc = GuideDoc(str(OUT))
    story = build_story(styles)
    doc.multiBuild(story)
    print(OUT)


if __name__ == "__main__":
    main()
