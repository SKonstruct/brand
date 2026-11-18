# brand

The shared look of the SKonstruct launchers (SKapsule for Android and iOS, SKradle for desktop): the app icon,
the logo glyph, the colour tokens and the legal line. Apps copy from here instead of from each other.

## Contents

- `icon/icon-1024.png`: the app icon, a full-bleed 1024 px square (pink ground, mint glyph), sRGB. Rendered from the SVG.
- `icon/logo.svg`: the glyph on its own, four pieces drawn as eight flat polygons in two groups: `<g id="outline">`
  (four `#75A09C` paths, painted first) and `<g id="fill">` (four `#C0DEDC` paths on top). The mint sits on the outline, so
  the glyph does not tint or fade as a whole; for a one-colour glyph use the outline paths alone. It has a `viewBox`
  (798 x 1105, the glyph inset 52 units) and no fixed width or height, so it scales to any size.
- `icon/android/ic_launcher_foreground.webp`: the Android adaptive-icon foreground (432 px, transparent).
- `icon/android/ic_launcher_monochrome.webp`: the same glyph as one silhouette, for Android 13 themed icons (alpha only).
- `tokens/colors.json`: the colours, below. Keys are `camelCase`; `spiralKnights` is the only group (flatten it as
  `spiralKnightsGold`, `--color-spiral-knights-gold`, and so on). Plain `#RRGGBB` sRGB, no alpha: an app that needs a
  translucent colour applies its own alpha to a token.
- `legal/disclaimer.md`: the line every app and page carries. Never claim affiliation with Grey Havens.
- `scripts/render.py`: draws the three raster files from `logo.svg`. `scripts/check.py`: the CI check.

## Colours

The palette is the dark theme the apps share. `pink` is the accent. It is only 4.0:1 on `ground`, so it is for fills,
large shapes and non-text parts; for pink text, icons and focus rings on dark surfaces use `pinkText`.

| Token | Hex | Use |
| --- | --- | --- |
| `ground` | `#000000` | Darkest background (OLED black). |
| `surface` | `#141414` | Default surface. |
| `surfaceElevated` | `#1E1E1E` | Cards and panels one step above `surface`. |
| `text` | `#FFFFFF` | Body text on any of the three above. |
| `textSecondary` | `#A6A6A6` | Secondary text on any of the three above. |
| `pink` | `#AB4A81` | Accent fill; `onPink` text on it is 5.2:1. |
| `pinkHover`, `pinkPressed` | `#B04F86`, `#963F6E` | The fill when hovered or pressed; `onPink` stays above 4.5:1. |
| `onPink` | `#FFFFFF` | Text and icons on a pink fill. |
| `pinkText` | `#E08BBB` | Pink text, icons and focus rings on dark surfaces (6.8:1 or more). |
| `error`, `success`, `warning` | `#FF7B72`, `#43CDCA`, `#F2BF3A` | Status colours; 6.6:1 or more on the dark surfaces. |
| `logoMint`, `logoOutline` | `#C0DEDC`, `#75A09C` | The glyph's two colours. |
| `amber`, `highlight` | `#F2BF3A`, `#FBC65B` | Warm accents. `amber` is also `warning`. |
| `spiralKnights.gold`, `spiralKnights.teal` | `#FFC134`, `#43CDCA` | The game's own colours, for places that should match the game. |

Light fills (mint, amber, gold, teal, `highlight`) take `ground` text, never white. State is never shown by colour alone.
`scripts/check.py` fails if a listed pairing drops below its contrast (4.5:1 for text, 3:1 for `pink` on `ground`).

## Using it

Apps copy the files they need and say in their own docs which commit of this repository they copied from; nothing is
linked at build time. When a file here changes, each app updates its copy on its own schedule.
`python3 scripts/check.py` (also run by CI, standard library only) checks the tokens and their contrast, the SVG, the
icon (a 1024 px PNG with an sRGB chunk) and the line endings.

To change the glyph, edit `icon/logo.svg` (plain `M`/`L`/`Z` paths, one subpath each) and run `python3 scripts/render.py`
(needs Pillow and numpy); commit the SVG and the three files it writes together.

Platform icons are made from `icon/icon-1024.png` by each app: iOS uses it as is, Android uses the foreground
on a pink ground, macOS uses Apple's template (the art at 824 of 1024 px with rounded corners and a soft shadow),
Windows and Linux use a full-bleed rounded square.

## License

[MIT](LICENSE)
