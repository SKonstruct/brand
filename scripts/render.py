#!/usr/bin/env python3
"""Renders the raster brand assets from icon/logo.svg, the single source of the glyph (needs Pillow and numpy).

    python3 scripts/render.py

Writes icon/icon-1024.png, icon/android/ic_launcher_foreground.webp and icon/android/ic_launcher_monochrome.webp.
The logo is flat polygons (M/L/Z only), so it is drawn directly: 8x supersampling with a premultiplied downsample,
exact token colours, no resampling blur. The placement constants below reproduce where the previous master icon and
Android foreground put the glyph (fitted from their pixels), so the apps' icons do not move.
"""
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, PngImagePlugin

ROOT = Path(__file__).resolve().parent.parent
PINK = (0xAB, 0x4A, 0x81)
OUTLINE = (0x75, 0xA0, 0x9C)
SS = 8  # supersampling factor
STRIP = 32  # output rows processed at a time

# (size px, scale from SVG units to px, x offset, y offset)
ICON = (1024, 0.5908, 279.68, 190.48)
ANDROID = (432, 0.25025, 116.77, 79.17)  # the 108 dp adaptive-icon layer at xxxhdpi


def parse(svg):
    """The glyph's polygons as [(fill, [(x, y), ...])] in paint order. Refuses anything but one M/L/Z subpath."""
    paths = []
    for m in re.finditer(r"<path\b([^>]*?)/?>", svg):
        fill = re.search(r'fill="#([0-9A-Fa-f]{6})"', m.group(1))
        d = re.search(r'\sd="([^"]+)"', m.group(1))
        if not fill or not d or set(re.findall(r"[A-Za-z]", d.group(1))) - set("MLZ") or d.group(1).count("M") != 1:
            sys.exit("scripts/render.py: logo.svg must hold plain M/L/Z polygons with a fill")
        pts = [(float(a), float(b)) for a, b in re.findall(r"(-?[\d.]+)[, ]\s*(-?[\d.]+)", d.group(1))]
        paths.append((tuple(int(fill.group(1)[i : i + 2], 16) for i in (0, 2, 4)), pts))
    return paths


def render(paths, layout, background=None, only_colour=None, colour=None):
    """RGBA image (straight alpha). `only_colour` keeps just the polygons of that fill and paints them in `colour`."""
    size, scale, ox, oy = layout
    big = Image.new("RGBA", (size * SS, size * SS), (0, 0, 0, 0))
    draw = ImageDraw.Draw(big)
    for fill, pts in paths:
        if only_colour is not None and fill != only_colour:
            continue
        poly = [((x * scale + ox) * SS, (y * scale + oy) * SS) for x, y in pts]
        draw.polygon(poly, fill=(colour or fill) + (255,))
    out = np.empty((size, size, 4), np.uint8)
    for y0 in range(0, size, STRIP):
        rows = np.asarray(big.crop((0, y0 * SS, size * SS, min(y0 + STRIP, size) * SS)), dtype=np.float32)
        h = rows.shape[0] // SS
        alpha = rows[..., 3:4] / 255.0
        premult = np.concatenate([rows[..., :3] * alpha, rows[..., 3:4]], axis=-1)
        premult = premult.reshape(h, SS, size, SS, 4).mean(axis=(1, 3))
        a = premult[..., 3:4]
        rgb = np.where(a > 0, premult[..., :3] / np.maximum(a / 255.0, 1e-6), 0)
        out[y0 : y0 + h] = np.rint(np.concatenate([rgb, a], axis=-1)).clip(0, 255).astype(np.uint8)
    image = Image.fromarray(out, "RGBA")
    if background is not None:
        flat = Image.new("RGBA", image.size, background + (255,))
        flat.alpha_composite(image)
        return flat.convert("RGB")
    # Where nothing is drawn keep a real colour, not black, so filtering at the edge cannot pull it dark.
    arr = np.asarray(image).copy()
    arr[arr[..., 3] == 0, :3] = colour or OUTLINE
    return Image.fromarray(arr, "RGBA")


def main():
    paths = parse((ROOT / "icon/logo.svg").read_text(encoding="utf-8"))

    info = PngImagePlugin.PngInfo()
    info.add(b"sRGB", b"\x00")  # perceptual rendering intent: the pixels are sRGB, as the tokens are
    render(paths, ICON, background=PINK).save(ROOT / "icon/icon-1024.png", pnginfo=info, optimize=True)

    for name, kwargs in {
        "ic_launcher_foreground": {},
        # Android 13 themed icons use only the alpha: the whole silhouette, the pieces still apart.
        "ic_launcher_monochrome": {"only_colour": OUTLINE, "colour": (0, 0, 0)},
    }.items():
        render(paths, ANDROID, **kwargs).save(
            ROOT / f"icon/android/{name}.webp", lossless=True, exact=True, quality=100, method=6
        )
    print("rendered icon-1024.png, ic_launcher_foreground.webp, ic_launcher_monochrome.webp")


if __name__ == "__main__":
    main()
