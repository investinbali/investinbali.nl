"""Generate smaller, content-addressed image variants without changing originals."""
import hashlib
import json
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', '.vercel', 'tmp', 'dist', 'assets', 'node_modules', 'seseh-construction-tracker'}


def main():
    sources = set()
    for page in ROOT.rglob('*.html'):
        if SKIP.intersection(page.relative_to(ROOT).parts):
            continue
        for tag in re.findall(r'<img\b[^>]*>', page.read_text(encoding='utf-8')):
            match = re.search(r'\bsrc="(/assets/[^"?]+)"', tag)
            if match and Path(match[1]).suffix.lower() in {'.webp', '.jpg', '.jpeg', '.png'}:
                sources.add(match[1])
    folder = ROOT / 'assets/responsive'
    folder.mkdir(exist_ok=True)
    manifest = {}
    for source in sorted(sources):
        original = ROOT / source.lstrip('/')
        digest = hashlib.sha256(original.read_bytes()).hexdigest()[:12]
        variants = []
        with Image.open(original) as image:
            for width in (480, 960, 1440):
                if width >= image.width:
                    continue
                output = folder / f'{original.stem}-{digest}-{width}.webp'
                if not output.exists():
                    resized = image.resize((width, round(image.height * width / image.width)), Image.Resampling.LANCZOS)
                    resized.save(output, 'WEBP', quality=82, method=6)
                variants.append({'src': '/' + output.relative_to(ROOT).as_posix(), 'width': width})
            variants.append({'src': source, 'width': image.width})
        manifest[source] = variants
    (ROOT / 'data/responsive-images.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(f'Prepared responsive variants for {len(manifest)} image sources')


if __name__ == '__main__':
    main()
