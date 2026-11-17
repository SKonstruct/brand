# brand

The shared look of the SKonstruct launchers (SKapsule for Android and iOS, SKradle for desktop): the app icon,
the logo glyph, the colour tokens and the legal line. Apps copy from here instead of from each other.

## Contents

- `icon/icon-1024.png`: the app icon, a full-bleed 1024 px square (pink ground, mint glyph).
- `icon/logo.svg`: the glyph on its own, four pieces: outline paths (`#75A09C`) first, then the mint paths (`#C0DEDC`).
- `icon/android/ic_launcher_foreground.webp`: the Android adaptive-icon foreground.
- `tokens/colors.json`: colours used across the apps. Pink `#AB4A81` is the accent.
- `legal/disclaimer.md`: the line every app and page carries. Never claim affiliation with Grey Havens.

Platform icons are made from `icon/icon-1024.png` by each app: iOS uses it as is, Android uses the foreground
on a pink ground, macOS uses Apple's template (the art at 824 of 1024 px with rounded corners and a soft shadow),
Windows and Linux use a full-bleed rounded square.

## License

[MIT](LICENSE)
