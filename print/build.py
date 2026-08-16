import base64, pathlib
SP = pathlib.Path('/tmp/claude-0/-home-user-hacking-geometry-syllabus/225411a4-975e-500e-8465-a2a4d4b2f999/scratchpad')
NM = SP / 'node_modules/@fontsource'

def b64(p, mime):
    return f"data:{mime};base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()

faces = []
for fam, w, style, fn in [
        ('Roboto', 400, 'normal', 'roboto/files/roboto-latin-400-normal.woff2'),
        ('Roboto', 700, 'normal', 'roboto/files/roboto-latin-700-normal.woff2'),
        ('Roboto', 400, 'italic', 'roboto/files/roboto-latin-400-italic.woff2'),
        ('Roboto', 700, 'italic', 'roboto/files/roboto-latin-700-italic.woff2'),
        ('JostGothic', 400, 'normal', 'jost/files/jost-latin-400-normal.woff2'),
        ('JostGothic', 700, 'normal', 'jost/files/jost-latin-700-normal.woff2')]:
    faces.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{style};"
                 f"src:url({b64(NM/fn,'font/woff2')}) format('woff2');}}")

body = (SP / 'body.html').read_text().replace('__LOGO__', b64(SP/'bac_logo.png','image/png'))

# Colors sampled from the Fall 2025 PDF
RULE_BLUE  = '#4F81BD'   # letterhead rule
TITLE_BLUE = '#006FC0'   # DME2100 - Hacking Geometry
GRAY_HEAD  = '#A6A6A6'   # grade table column header row
LINK_BLUE  = '#1155CC'   # hyperlinks

html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>DME2100 Hacking Geometry Syllabus Fall 2026</title>
<style>
{chr(10).join(faces)}
@page {{ size: Letter; margin: 0.8in 0.9in 0.75in 0.9in; }}
* {{ box-sizing: border-box; }}
body {{ font-family: Roboto, Arial, sans-serif; font-size: 10pt; line-height: 12pt;
        color: #000; margin: 0; text-align: left; }}
p {{ margin: 0 0 12pt 0; }}
b {{ font-weight: 700; }}
.letterhead img {{ width: 165pt; height: auto; display: block; margin-bottom: 2pt; }}
.rule {{ font-family: Arial, 'Liberation Sans', sans-serif; font-weight: 700; font-size: 12pt;
         letter-spacing: -0.2pt; margin: 0 0 16pt 0; overflow: hidden;
         white-space: nowrap; color: {RULE_BLUE}; }}
.doctitle {{ font-size: 14pt; font-weight: 700; color: {TITLE_BLUE}; margin: 0 0 14pt 0; }}
.syllabus {{ font-size: 15pt; font-weight: 700; text-align: center; margin: 0 0 16pt 0; }}
.meta {{ margin: 0 0 12pt 0; line-height: 14pt; }}
.secnum {{ font-size: 12pt; font-weight: 700; text-decoration: underline;
           text-underline-offset: 2pt; margin: 16pt 0 12pt 0;
           break-after: avoid; page-break-after: avoid; }}
ol, ul {{ margin: 0 0 12pt 0; padding-left: 24pt; }}
li {{ margin-bottom: 0; }}
ol.spaced li, ul.spaced li {{ margin-bottom: 6pt; }}
.dates {{ margin: 0 0 12pt 0; }}
.small {{ font-size: 8pt; line-height: 10pt; }}
.pagebreak {{ break-before: page; page-break-before: always; }}
a, a:visited {{ color: {LINK_BLUE}; text-decoration: underline; }}
table {{ border-collapse: collapse; width: 100%; margin: 0 0 12pt 0; }}
table.sched td {{ vertical-align: top; padding: 3pt 6pt 3pt 0; border-bottom: 0.5pt solid #A6A6A6; }}
table.sched td.d {{ width: 78pt; font-weight: 700; white-space: nowrap; }}
table.sched td.hl {{ background: #EDEDED; }}

table.grades {{ font-family: 'JostGothic', 'Century Gothic', Roboto, sans-serif;
                font-size: 8pt; line-height: 10pt; font-weight: 700; }}
table.grades td {{ border: 0.75pt solid #000; padding: 2.5pt 4pt; vertical-align: top;
                   text-align: left; }}
table.grades tr.band td {{ background: #000; color: #fff; border-color: #000; }}
table.grades tr.colhead td {{ background: {GRAY_HEAD}; }}
table.grades tr:not(.band) td:nth-child(1) {{ width: 62pt; }}
table.grades tr:not(.band) td:nth-child(2) {{ width: 58pt; }}
table.grades tr:not(.band) td:nth-child(3) {{ width: 62pt; }}
tr {{ break-inside: avoid; page-break-inside: avoid; }}
.keep {{ break-inside: avoid; page-break-inside: avoid; }}
p, li {{ orphans: 2; widows: 2; }}
</style></head><body>
{body}
</body></html>"""

out = pathlib.Path('/home/user/hacking-geometry-syllabus/print/syllabus.html')
out.write_text(html)
print('wrote', out, len(html) // 1024, 'KB')
