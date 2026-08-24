#!/usr/bin/env python3
"""
frame_portrait.py - wraps assets/portrait.svg in a padded frame with an
animated dashed border (SMIL animation, renders natively on GitHub).

Usage:
    python scripts/frame_portrait.py --src assets/portrait.svg --out assets/portrait-framed.svg
"""
import argparse
import re

def get_wh(svg_text):
    vb = re.search(r'viewBox="([\d.\-]+) ([\d.\-]+) ([\d.\-]+) ([\d.\-]+)"', svg_text)
    if vb:
        return float(vb.group(3)), float(vb.group(4))
    w = re.search(r'width="([\d.]+)', svg_text)
    h = re.search(r'height="([\d.]+)', svg_text)
    return float(w.group(1)), float(h.group(1))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="assets/portrait.svg")
    ap.add_argument("--out", default="assets/portrait-framed.svg")
    ap.add_argument("--padding", type=float, default=28)
    ap.add_argument("--color", default="#F97316", help="border accent color, hex")
    ap.add_argument("--radius", type=float, default=18, help="corner radius")
    ap.add_argument("--duration", default="6s", help="one full dash-rotation cycle")
    args = ap.parse_args()

    with open(args.src, "r", encoding="utf-8") as f:
        src_text = f.read()

    w, h = get_wh(src_text)
    pad = args.padding
    total_w = w + pad * 2
    total_h = h + pad * 2
    perim = 2 * (total_w + total_h - 4 * args.radius) + 2 * 3.14159 * args.radius

    framed = f'''<svg viewBox="0 0 {total_w} {total_h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <clipPath id="roundedFrame">
      <rect x="0" y="0" width="{total_w}" height="{total_h}" rx="{args.radius + 6}" />
    </clipPath>
  </defs>

  <image href="{args.src.split('/')[-1]}" x="{pad}" y="{pad}" width="{w}" height="{h}" clip-path="url(#roundedFrame)" />

  <rect x="2" y="2" width="{total_w - 4}" height="{total_h - 4}" rx="{args.radius}"
        fill="none" stroke="{args.color}" stroke-width="3"
        stroke-dasharray="14 8" stroke-linecap="round">
    <animate attributeName="stroke-dashoffset" from="0" to="{perim:.0f}"
             dur="{args.duration}" repeatCount="indefinite" />
  </rect>
</svg>'''

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(framed)

    print(f"wrote {args.out}  ({total_w:.0f}x{total_h:.0f}, padding={pad:.0f}px)")

if __name__ == "__main__":
    main()
