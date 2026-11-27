#!/usr/bin/env python3
"""Generate responsive WebP variants, JPEG fallbacks and the Open Graph image.

Reads originals from photos/, writes to photos/opt/ and records the generated
variants in photos/opt/manifest.json, which tools/build_site.py consumes.

Usage: python3 tools/build_images.py   (requires Pillow with WebP support)
"""
import json
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "photos"
OUT = SRC / "opt"

WIDTHS = [480, 800, 1200, 1600]
# Wide variants are mostly picked by high-DPR phones, where lower quality is not visible.
WEBP_QUALITY = {480: 74, 800: 72, 1200: 64, 1600: 62}
JPEG_QUALITY = 74
FALLBACK_WIDTH = 800

# key -> (source file, optional crop box). img45/img7 are phone screenshots;
# the crop keeps only the photo and drops the black bars and viewer UI.
IMAGES = {
    "hotel-ansicht": ("hotel-ansicht.jpeg", None),
    "fethiye-bay": ("nakas-hotel.jpg", None),
    "penthouse": ("img30.jpeg", None),
    "standard": ("img40.jpeg", None),
    "garden": ("garten.jpeg", None),
    "room-sofa": ("img45.jpeg", (0, 606, 738, 1016)),
    "bed": ("wa1.jpeg", None),
    "balcony": ("img35.jpeg", None),
    "room": ("img20.jpeg", None),
    "bathroom": ("img15.jpeg", None),
    "washbasin": ("img7.jpeg", (0, 606, 738, 1016)),
    "bath": ("img10.jpeg", None),
    "oludeniz": ("olüdeniz-foto.jpg", None),
}


def load(name, crop):
    im = ImageOps.exif_transpose(Image.open(SRC / name)).convert("RGB")
    return im.crop(crop) if crop else im


def resized(im, width):
    if width >= im.width:
        return im
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


def build_photo(key, name, crop):
    im = load(name, crop)
    widths = [w for w in WIDTHS if w < im.width] + [min(im.width, WIDTHS[-1])]
    variants = []
    for w in sorted(set(widths)):
        out = resized(im, w)
        path = OUT / f"{key}-{w}.webp"
        quality = WEBP_QUALITY.get(w, WEBP_QUALITY[min(WEBP_QUALITY, key=lambda k: abs(k - w))])
        out.save(path, "WEBP", quality=quality, method=6)
        variants.append({"w": w, "h": out.height, "src": f"/photos/opt/{path.name}"})
    fb = resized(im, min(FALLBACK_WIDTH, im.width))
    fb_path = OUT / f"{key}-{fb.width}.jpg"
    fb.save(fb_path, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    return {
        "width": variants[-1]["w"],
        "height": variants[-1]["h"],
        "webp": variants,
        "fallback": {"w": fb.width, "h": fb.height, "src": f"/photos/opt/{fb_path.name}"},
    }


def build_logo():
    im = Image.open(SRC / "nakas-logo.png").convert("RGBA")
    im = im.resize((160, 160), Image.LANCZOS)
    im.save(OUT / "nakas-logo-160.png", optimize=True)
    im.save(OUT / "nakas-logo-160.webp", "WEBP", quality=90, method=6)
    return {"width": 160, "height": 160, "png": "/photos/opt/nakas-logo-160.png",
            "webp": "/photos/opt/nakas-logo-160.webp"}


def build_og():
    im = load("hotel-ansicht.jpeg", None)
    im = resized(im, 1200)
    top = round((im.height - 630) * 0.35)
    og = im.crop((0, top, 1200, top + 630))
    path = OUT / "og-nakas-hotel-1200x630.jpg"
    og.save(path, "JPEG", quality=80, optimize=True, progressive=True)
    return {"width": 1200, "height": 630, "src": f"/photos/opt/{path.name}"}


def main():
    OUT.mkdir(exist_ok=True)
    manifest = {"photos": {}, "logo": build_logo(), "og": build_og()}
    for key, (name, crop) in IMAGES.items():
        manifest["photos"][key] = build_photo(key, name, crop)
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    total = sum(p.stat().st_size for p in OUT.iterdir())
    print(f"wrote {len(list(OUT.iterdir()))} files, {total // 1024} KB")


if __name__ == "__main__":
    main()
