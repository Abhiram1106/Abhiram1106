#!/usr/bin/env python3
"""
about_card.py - generates a centered, professionally-spaced "About Me" info
card SVG matching the dark-navy / orange-accent look of the other cards.
Stdlib only.

Usage:
    python scripts/about_card.py -o assets/about-card.svg
"""
import argparse
import textwrap
from xml.sax.saxutils import escape

def wrap(text, width):
    return textwrap.wrap(text, width=width) or [""]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default="assets/about-card.svg")
    ap.add_argument("--bg", default="#0f172a")
    ap.add_argument("--border", default="#F97316")
    ap.add_argument("--title-color", default="#e2e8f0")
    ap.add_argument("--label-color", default="#F97316")
    ap.add_argument("--value-color", default="#94a3b8")
    ap.add_argument("--divider-color", default="#1e293b")
    ap.add_argument("--width", type=int, default=640)
    args = ap.parse_args()

    rows = [
        ("🎯", "Role", "Software Engineer"),
        ("📍", "Location", "Andhra Pradesh, India"),
        ("🔨", "Currently", "Building Vizag Forever @ Technopose"),
        ("🧠", "Focus", "Learning System Design, AWS, and scalable application building"),
        ("🚀", "Open to", "Full-time and Internship roles - graduating 2027"),
    ]

    W = args.width
    cx = W / 2
    title_h = 64
    label_line_h = 26   # space from label baseline to first value line
    value_line_h = 22   # spacing between wrapped value lines
    row_top_pad = 34     # space above each row's label
    row_bottom_pad = 22  # space after last value line before divider
    value_wrap_chars = 52

    y = title_h
    row_blocks = []
    for icon, label, value in rows:
        lines = wrap(value, value_wrap_chars)
        label_y = y + row_top_pad
        first_value_y = label_y + label_line_h
        block_bottom = first_value_y + (len(lines) - 1) * value_line_h + row_bottom_pad
        row_blocks.append((icon, label, lines, label_y, first_value_y, block_bottom))
        y = block_bottom

    H = y + 16

    svg_parts = []
    svg_parts.append(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">')
    svg_parts.append(f'''  <defs>
    <linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{args.border}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{args.border}" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="{args.border}" stop-opacity="0"/>
    </linearGradient>
  </defs>''')

    # outer card
    svg_parts.append(
        f'  <rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="18" '
        f'fill="{args.bg}" stroke="{args.border}" stroke-width="1.5"/>'
    )
    # title band
    svg_parts.append(f'  <rect x="1.5" y="1.5" width="{W-3}" height="{title_h}" rx="18" fill="url(#titleGrad)"/>')
    svg_parts.append(
        f'  <text x="{cx}" y="{title_h/2 + 9}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
        f'font-size="24" font-weight="700" fill="{args.title_color}">{escape("👋  About Me")}</text>'
    )
    svg_parts.append(f'  <line x1="24" y1="{title_h+1}" x2="{W-24}" y2="{title_h+1}" stroke="{args.border}" stroke-opacity="0.35" stroke-width="1"/>')

    for idx, (icon, label, lines, label_y, first_value_y, block_bottom) in enumerate(row_blocks):
        svg_parts.append(
            f'  <text x="{cx}" y="{label_y}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
            f'font-size="16" font-weight="700" fill="{args.label_color}">{escape(icon)}  {escape(label)}</text>'
        )
        for i, line in enumerate(lines):
            svg_parts.append(
                f'  <text x="{cx}" y="{first_value_y + i*value_line_h}" text-anchor="middle" '
                f'font-family="Segoe UI, Arial, sans-serif" font-size="14.5" '
                f'fill="{args.value_color}">{escape(line)}</text>'
            )
        if idx < len(row_blocks) - 1:
            divider_y = block_bottom - row_bottom_pad / 2
            svg_parts.append(
                f'  <line x1="60" y1="{divider_y}" x2="{W-60}" y2="{divider_y}" '
                f'stroke="{args.divider_color}" stroke-width="1"/>'
            )

    svg_parts.append('</svg>')
    svg = "\n".join(svg_parts)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"wrote {args.out}  ({W}x{H})")

if __name__ == "__main__":
    main()