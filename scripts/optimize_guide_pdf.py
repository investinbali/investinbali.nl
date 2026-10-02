"""Compress guide photos while preserving selectable text, page geometry and links.

Usage: python scripts/optimize_guide_pdf.py input.pdf output.pdf
Output must differ from input so the original remains available for visual review.
"""
import io
import sys
from pathlib import Path
import fitz
from PIL import Image


def optimize(source, target):
    if source.resolve() == target.resolve():
        raise ValueError('Use a separate output, inspect it, then publish it')
    doc = fitz.open(source)
    texts = [p.get_text() for p in doc]
    links = [len(p.get_links()) for p in doc]
    seen = set()
    for page in doc:
        for entry in page.get_images(full=True):
            xref, smask = entry[:2]
            if xref in seen or smask:
                continue
            seen.add(xref)
            raw = doc.extract_image(xref)['image']
            with Image.open(io.BytesIO(raw)) as image:
                if max(image.size) < 900:
                    continue
                image = image.convert('RGB')
                image.thumbnail((1400, 1400), Image.Resampling.LANCZOS)
                buf = io.BytesIO()
                image.save(buf, 'JPEG', quality=82, optimize=True)
                if len(buf.getvalue()) < len(raw):
                    page.replace_image(xref, stream=buf.getvalue())
    target.parent.mkdir(parents=True, exist_ok=True)
    doc.save(target, garbage=4, deflate=True)
    doc.close()
    check = fitz.open(target)
    assert texts == [p.get_text() for p in check], 'Text changed during compression'
    assert links == [len(p.get_links()) for p in check], 'Links changed during compression'
    assert len(texts) == len(check)
    # Contact sheet for all pages plus detailed examples; not part of the published PDF.
    sheet = Image.new('RGB', (1000, ((len(check) + 3) // 4) * 365), 'white')
    for n, page in enumerate(check):
        pix = page.get_pixmap(matrix=fitz.Matrix(.4, .4), alpha=False)
        thumb = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        sheet.paste(thumb, ((n % 4) * 250, (n // 4) * 365))
    sheet.save(target.parent / 'guide-contact-sheet.png')
    for n in (0, 4, len(check) - 1):
        check[n].get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False).save(target.parent / f'guide-page-{n+1}.png')
    print(f'{len(check)} pages; text and links unchanged; {source.stat().st_size} -> {target.stat().st_size} bytes')


if __name__ == '__main__':
    optimize(Path(sys.argv[1]), Path(sys.argv[2]))
