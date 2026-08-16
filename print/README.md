# Print syllabus

Source for `DME2100_Hacking_Geometry_Fall2026.pdf`, matched to the Fall 2025
syllabus template: US Letter, 0.9in side margins, Roboto at 10pt body / 12pt
section headings / 14pt title, and the BAC letterhead extracted from the
Fall 2025 PDF.

- `body.html` is the content. Edit this.
- `build.py` inlines the fonts and logo and writes `syllabus.html`.
- `syllabus.html` is generated. Do not edit by hand.
- `bac_logo.png` is the letterhead.

## Rebuild

Requires `@fontsource/roboto` (npm) for the Roboto woff2 files and a Chromium
with Playwright. Adjust the font path at the top of `build.py` if needed.

    python3 build.py
    node render.js

`render.js` loads `syllabus.html` in Chromium and prints to PDF at Letter size
with a page-number footer.
