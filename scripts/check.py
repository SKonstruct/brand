#!/usr/bin/env python3
"""Checks the brand files: the tokens parse, are colours and keep the contrast the README promises for each pairing,
the SVG is well-formed and sized only by its viewBox, the icon is the 1024 px sRGB square the apps expect, and every text
file ends with a newline. Standard library only."""
import json, re, struct, sys, xml.etree.ElementTree as ET
from pathlib import Path

root = Path(__file__).resolve().parent.parent
problems = []

def colours(node, where="tokens/colors.json"):
    for key, value in node.items():
        if isinstance(value, dict):
            colours(value, f"{where}.{key}")
        elif not re.fullmatch(r"#[0-9A-Fa-f]{6}", str(value)):
            problems.append(f"{where}.{key} is not a #RRGGBB colour: {value!r}")

# (text or fill colour, background, minimum WCAG 2.1 contrast, what it is for). Keep in step with the README table.
PAIRS = [
    ("text", "ground", 4.5, "body text"),
    ("text", "surface", 4.5, "body text"),
    ("text", "surfaceElevated", 4.5, "body text"),
    ("textSecondary", "ground", 4.5, "secondary text"),
    ("textSecondary", "surface", 4.5, "secondary text"),
    ("textSecondary", "surfaceElevated", 4.5, "secondary text"),
    ("pinkText", "ground", 4.5, "pink text, icons and focus rings"),
    ("pinkText", "surface", 4.5, "pink text, icons and focus rings"),
    ("pinkText", "surfaceElevated", 4.5, "pink text, icons and focus rings"),
    ("onPink", "pink", 4.5, "text on a pink fill"),
    ("onPink", "pinkHover", 4.5, "text on a hovered pink fill"),
    ("onPink", "pinkPressed", 4.5, "text on a pressed pink fill"),
    ("error", "ground", 4.5, "error text"),
    ("error", "surface", 4.5, "error text"),
    ("error", "surfaceElevated", 4.5, "error text"),
    ("success", "surface", 4.5, "success text"),
    ("success", "surfaceElevated", 4.5, "success text"),
    ("warning", "surface", 4.5, "warning text"),
    ("warning", "surfaceElevated", 4.5, "warning text"),
    ("pink", "ground", 3.0, "pink as a large or non-text element only"),
]

def flat(node, prefix=""):
    for key, value in node.items():
        if isinstance(value, dict):
            yield from flat(value, f"{prefix}{key}.")
        else:
            yield f"{prefix}{key}", value

def luminance(hex_colour):
    def channel(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(int(hex_colour[i : i + 2], 16)) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)

try:
    tokens = json.loads((root / "tokens/colors.json").read_text(encoding="utf-8"))
    colours(tokens)
    table = dict(flat(tokens))
    for fg, bg, minimum, use in PAIRS:
        if fg not in table or bg not in table:
            problems.append(f"tokens/colors.json: {fg} or {bg} is missing (needed for {use})")
        elif (ratio := contrast(table[fg], table[bg])) < minimum:
            problems.append(f"tokens/colors.json: {fg} on {bg} is {ratio:.2f}:1, below {minimum}:1 ({use})")
except (OSError, ValueError, TypeError) as e:
    problems.append(f"tokens/colors.json: {e}")

try:
    svg = ET.parse(root / "icon/logo.svg").getroot()
    if not svg.tag.endswith("svg"):
        problems.append("icon/logo.svg: the root element is not <svg>")
    if "viewBox" not in svg.attrib:
        problems.append("icon/logo.svg: no viewBox")
    if "width" in svg.attrib or "height" in svg.attrib:
        problems.append("icon/logo.svg: fixed width/height; size it with the viewBox only")
except (OSError, ET.ParseError) as e:
    problems.append(f"icon/logo.svg: {e}")

try:
    png = (root / "icon/icon-1024.png").read_bytes()
    if png[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", png[16:24]) != (1024, 1024):
        problems.append("icon/icon-1024.png is not a 1024 x 1024 PNG")
    else:
        chunks, at = [], 8
        while at + 8 <= len(png):
            size = struct.unpack(">I", png[at : at + 4])[0]
            chunks.append(png[at + 4 : at + 8])
            at += 12 + size
        if b"sRGB" not in chunks:
            problems.append("icon/icon-1024.png has no sRGB chunk; render it with scripts/render.py")
except OSError as e:
    problems.append(f"icon/icon-1024.png: {e}")

for path in [*root.glob("*.md"), *root.glob("legal/*.md"), *root.glob("tokens/*.json"), root / "icon/logo.svg"]:
    data = path.read_bytes()
    if data and not data.endswith(b"\n"):
        problems.append(f"{path.relative_to(root)} does not end with a newline")
    if b"\r\n" in data:
        problems.append(f"{path.relative_to(root)} has CRLF line endings")

for p in problems:
    print("brand check:", p)
sys.exit(1 if problems else 0)
