# Print syllabus

Source for `DME2100_Hacking_Geometry_Fall2026.pdf`, matched to the Fall 2025
syllabus template.

## Template spec, measured from the Fall 2025 PDF

- US Letter, 0.9in side margins, 0.8in top, 0.75in bottom
- Roboto: 10pt body on 12pt leading, 12pt underlined section headings,
  14pt title, 15pt centered SYLLABUS
- Letterhead rule `#4F81BD`, title `#006FC0`, hyperlinks `#1155CC`,
  grade-table column header `#A6A6A6`, institutional band black on white
- Page numbers bottom right, omitted on page 1
- `bac_logo.png` is the letterhead image extracted from the Fall 2025 PDF

The grade table in the Fall 2025 original is set in Century Gothic Bold, a
licensed Monotype face. Jost is substituted as the closest freely available
geometric sans.

## Files

- `body.html` is the content. Edit this.
- `build.py` inlines the fonts and logo and writes `syllabus.html`.
- `syllabus.html` is generated. Do not edit by hand.
- `render.js` prints `syllabus.html` to PDF.

## Rebuild

Needs `@fontsource/roboto`, `@fontsource/jost`, `playwright-core`, and
`pdf-lib` from npm, plus a Chromium binary. Set `CHROMIUM_PATH` if it is not
at `/opt/pw-browsers/chromium`. Adjust the font path at the top of `build.py`
to point at your `node_modules/@fontsource`.

    python3 print/build.py
    node print/render.js
