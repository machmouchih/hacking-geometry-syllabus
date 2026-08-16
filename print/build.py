import base64, pathlib
SP = pathlib.Path('/tmp/claude-0/-home-user-hacking-geometry-syllabus/225411a4-975e-500e-8465-a2a4d4b2f999/scratchpad')
FD = SP / 'node_modules/@fontsource/roboto/files'

def b64(p, mime):
    return f"data:{mime};base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()

faces = []
for w, style, fn in [(400,'normal','roboto-latin-400-normal.woff2'),
                     (700,'normal','roboto-latin-700-normal.woff2'),
                     (400,'italic','roboto-latin-400-italic.woff2'),
                     (700,'italic','roboto-latin-700-italic.woff2')]:
    faces.append(f"@font-face{{font-family:Roboto;font-weight:{w};font-style:{style};"
                 f"src:url({b64(FD/fn,'font/woff2')}) format('woff2');}}")

body = (SP / 'body.html').read_text().replace('__LOGO__', b64(SP/'bac_logo.png','image/png'))

html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>DME2100 Hacking Geometry Syllabus Fall 2026</title>
<style>
{chr(10).join(faces)}
@page {{ size: Letter; margin: 0.8in 0.9in 0.75in 0.9in; }}
* {{ box-sizing: border-box; }}
body {{ font-family: Roboto, Arial, sans-serif; font-size: 10pt; line-height: 1.35;
        color: #000; margin: 0; text-align: left; }}
p {{ margin: 0 0 10pt 0; }}
b {{ font-weight: 700; }}
.letterhead img {{ width: 165pt; height: auto; display: block; margin-bottom: 2pt; }}
.rule {{ font-family: Arial, sans-serif; font-weight: 700; font-size: 12pt;
         letter-spacing: -0.3pt; margin: 0 0 14pt 0; overflow: hidden;
         white-space: nowrap; color: #000; }}
.doctitle {{ font-size: 14pt; font-weight: 700; margin: 0 0 12pt 0; }}
.syllabus {{ font-size: 15pt; font-weight: 700; text-align: center; margin: 0 0 14pt 0; }}
.meta {{ margin: 0 0 12pt 0; }}
.secnum {{ font-size: 12pt; font-weight: 700; margin: 16pt 0 10pt 0;
           break-after: avoid; page-break-after: avoid; }}
ol, ul {{ margin: 0 0 10pt 0; padding-left: 22pt; }}
li {{ margin-bottom: 5pt; }}
ul.tight li {{ margin-bottom: 1pt; }}
.dates {{ margin: 0 0 10pt 0; }}
.small {{ font-size: 8pt; line-height: 1.3; }}
.pagebreak {{ break-before: page; page-break-before: always; }}
table {{ border-collapse: collapse; width: 100%; margin: 0 0 12pt 0; }}
table.sched td {{ vertical-align: top; padding: 3pt 6pt 3pt 0; border-bottom: 0.5pt solid #ccc; }}
table.sched td.d {{ width: 78pt; font-weight: 700; white-space: nowrap; }}
table.sched td.hl {{ background: #f0f0f0; }}
table.grades {{ font-size: 8.5pt; line-height: 1.25; }}
table.grades th, table.grades td {{ border: 0.5pt solid #999; padding: 3pt 4pt;
                                    vertical-align: top; text-align: left; }}
table.grades th {{ font-weight: 700; background: #f0f0f0; }}
table.grades td:nth-child(1), table.grades td:nth-child(2), table.grades td:nth-child(3) {{
    white-space: nowrap; width: 52pt; }}
tr {{ break-inside: avoid; page-break-inside: avoid; }}
.keep {{ break-inside: avoid; page-break-inside: avoid; }}
p, li {{ orphans: 2; widows: 2; }}
</style></head><body>
{body}
</body></html>"""

out = pathlib.Path('/home/user/hacking-geometry-syllabus/print/syllabus.html')
out.write_text(html)
print('wrote', out, len(html) // 1024, 'KB')
