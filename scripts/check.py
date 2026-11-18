#!/usr/bin/env python3
"""Checks the brand files: the tokens parse and are colours, the SVG is well-formed and sized only by its viewBox, the
icon is the 1024 px square the apps expect, and every text file ends with a newline."""
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

try:
    colours(json.loads((root / "tokens/colors.json").read_text(encoding="utf-8")))
except (OSError, ValueError) as e:
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
    head = (root / "icon/icon-1024.png").read_bytes()[:24]
    if head[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", head[16:24]) != (1024, 1024):
        problems.append("icon/icon-1024.png is not a 1024 x 1024 PNG")
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
