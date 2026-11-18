# brand

The shared look of the SKonstruct launchers (SKapsule for Android and iOS, SKradle for desktop): the app icon,
the logo glyph, the colour tokens and the legal line. Apps copy from here instead of from each other.

## Contents

- `icon/icon-1024.png`: the app icon, a full-bleed 1024 px square (pink ground, mint glyph).
- `icon/logo.svg`: the glyph on its own, four pieces drawn as eight paths: the four outline paths (`#75A09C`) first, then
  the four mint paths (`#C0DEDC`). It has a `viewBox` and no fixed width or height, so it scales to any size.
- `icon/android/ic_launcher_foreground.webp`: the Android adaptive-icon foreground.
- `tokens/colors.json`: colours used across the apps. `pink` (`#AB4A81`) is the accent; `ground`, `surface`, `text` and
  `textSecondary` are the dark theme's background layers and text; `logoMint` and `logoOutline` are the glyph's two
  colours; `amber` and `highlight` are warm accents; `spiralKnights.gold` and `spiralKnights.teal` are the game's own
  colours, for places that should match the game.
- `legal/disclaimer.md`: the line every app and page carries. Never claim affiliation with Grey Havens.

## Using it

Apps copy the files they need and say in their own docs which commit of this repository they copied from; nothing is
linked at build time. When a file here changes, each app updates its copy on its own schedule.
`python3 scripts/check.py` (also run by CI) checks that the tokens are colours, the SVG is well-formed and sized by its
`viewBox` alone, the icon is a 1024 px PNG, and the text files end with a newline.

Platform icons are made from `icon/icon-1024.png` by each app: iOS uses it as is, Android uses the foreground
on a pink ground, macOS uses Apple's template (the art at 824 of 1024 px with rounded corners and a soft shadow),
Windows and Linux use a full-bleed rounded square.

## License

[MIT](LICENSE)
