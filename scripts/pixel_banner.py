#!/usr/bin/env python3
"""
pixel_banner.py - renders text as a chunky pixel/LED-matrix style banner PNG.
Supports multi-line text: pass \\n in --text to break lines.
Stdlib + Pillow only.

Usage (single line):
    python scripts/pixel_banner.py --text "JONNADULA ABHIRAM" -o assets/banner.png

Usage (two lines):
    python scripts/pixel_banner.py --text "JONNADULA`nABHIRAM" -o assets/banner.png
    (in PowerShell, use a backtick-n for a real newline inside a double-quoted string)
"""
import argparse
import os
from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = [
    "C:\\Windows\\Fonts\\arialbd.ttf",
    "C:\\Windows\\Fonts\\seguisb.ttf",
    "C:\\Windows\\Fonts\\calibrib.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
]

def load_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size), path
    return None, None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True, help="use \\n for a line break")
    ap.add_argument("-o", "--out", default="assets/banner.png")
    ap.add_argument("--bg", default="#0b1220")
    ap.add_argument("--fg", default="#e2e8f0")
    ap.add_argument("--pixel", type=int, default=5)
    ap.add_argument("--font-size", type=int, default=90)
    ap.add_argument("--padding", type=int, default=40)
    ap.add_argument("--line-spacing", type=int, default=10)
    ap.add_argument("--align", default="center", choices=["left", "center", "right"])
    ap.add_argument("--font", default=None)
    args = ap.parse_args()

    text = args.text.replace("\\n", "\n")  # handle literal backslash-n too
    scale_down = args.pixel
    big_size = args.font_size

    if args.font:
        font = ImageFont.truetype(args.font, big_size)
        used = args.font
    else:
        font, used = load_font(big_size)
        if font is None:
            raise SystemExit(
                "No usable bold .ttf font found. Pass one explicitly with --font."
            )

    print(f"using font: {used}")

    tmp = Image.new("RGB", (10, 10))
    d = ImageDraw.Draw(tmp)
    bbox = d.multiline_textbbox((0, 0), text, font=font, spacing=args.line_spacing, align=args.align)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    full_w = text_w + args.padding * 2
    full_h = text_h + args.padding * 2

    img = Image.new("RGB", (full_w, full_h), args.bg)
    draw = ImageDraw.Draw(img)
    draw.multiline_text(
        (args.padding - bbox[0], args.padding - bbox[1]),
        text, font=font, fill=args.fg,
        spacing=args.line_spacing, align=args.align,
    )

    small = img.resize((max(1, full_w // scale_down), max(1, full_h // scale_down)), Image.BILINEAR)
    pixelated = small.resize((full_w, full_h), Image.NEAREST)

    pixelated.save(args.out)
    print(f"wrote {args.out}  ({full_w}x{full_h}, pixel={args.pixel}, font_size={big_size})")

if __name__ == "__main__":
    main()