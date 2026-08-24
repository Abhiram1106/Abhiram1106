#!/usr/bin/env python3
"""
composite_calendar.py - injects an image as a genuine background layer
INSIDE the metrics.isocalendar.svg file, so it renders behind the calendar
bars (SVG draws elements in document order - earlier = further back).

This runs as a workflow step, AFTER the metrics action has generated and
committed the plain calendar, so it works on every scheduled run and keeps
the calendar's data live while achieving real layering (not just adjacent
placement - the background image is inside the same <svg> element).

Usage:
    python scripts/composite_calendar.py \
        --svg assets/metrics.isocalendar.svg \
        --bg-image assets/spiderman.png \
        --opacity 0.15
"""
import argparse
import base64
import re
import mimetypes

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--svg", required=True)
    ap.add_argument("--bg-image", required=True)
    ap.add_argument("--opacity", type=float, default=0.18,
                     help="keep low (0.1-0.25) so calendar bars stay readable on top")
    ap.add_argument("--x", type=float, default=None, help="x position; default = left-bottom area")
    ap.add_argument("--y", type=float, default=None, help="y position; default = left-bottom area")
    ap.add_argument("--size", type=float, default=140, help="rendered width/height of the bg image")
    args = ap.parse_args()

    with open(args.svg, "r", encoding="utf-8") as f:
        svg_text = f.read()

    # already composited? don't double-inject on repeated runs
    if 'id="bg-layer-injected"' in svg_text:
        print("background layer already present, skipping re-injection")
        return

    vb = re.search(r'viewBox="([\d.\-]+) ([\d.\-]+) ([\d.\-]+) ([\d.\-]+)"', svg_text)
    if not vb:
        raise SystemExit("could not find viewBox in target SVG - aborting")
    vb_x, vb_y, vb_w, vb_h = map(float, vb.groups())

    x = args.x if args.x is not None else vb_x + 10
    y = args.y if args.y is not None else vb_y + vb_h - args.size - 10

    with open(args.bg_image, "rb") as f:
        img_bytes = f.read()
    mime = mimetypes.guess_type(args.bg_image)[0] or "image/png"
    b64 = base64.b64encode(img_bytes).decode("ascii")
    data_uri = f"data:{mime};base64,{b64}"

    bg_element = (
        f'<image id="bg-layer-injected" href="{data_uri}" '
        f'x="{x}" y="{y}" width="{args.size}" height="{args.size}" '
        f'opacity="{args.opacity}" />'
    )

    # insert right after the opening <svg ...> tag so it's the FIRST drawn
    # element - everything else in the file (the calendar) then draws on top
    new_svg = re.sub(r'(<svg[^>]*>)', r'\1' + bg_element, svg_text, count=1)

    with open(args.svg, "w", encoding="utf-8") as f:
        f.write(new_svg)

    print(f"injected background layer into {args.svg} at ({x:.0f},{y:.0f}), size={args.size}, opacity={args.opacity}")

if __name__ == "__main__":
    main()
