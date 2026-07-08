"""Build the complete AI-901 course PDF from the module markdown files.

1. Converts modules/*.md to HTML (with SVG diagrams inlined).
2. Renders course.html to pdf/AI-901-Complete-Course.pdf via headless Edge.

Run:  python build_pdf.py
"""
import glob
import os
import re
import subprocess

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MODULES = os.path.join(ROOT, "modules")
DIAGRAMS = os.path.join(ROOT, "diagrams")
OUT_HTML = os.path.join(HERE, "course.html")
OUT_PDF = os.path.join(ROOT, "pdf", "AI-901-Complete-Course.pdf")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

CSS = """
@page { size: A4; margin: 18mm 16mm; }
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', Arial, sans-serif; color: #16324f; font-size: 11.5pt;
       line-height: 1.55; margin: 0; }
h1 { font-size: 22pt; color: #0b5cab; border-bottom: 3px solid #0b5cab;
     padding-bottom: 6px; margin: 0 0 14px; }
h2 { font-size: 15pt; color: #0b5cab; margin: 22px 0 8px; }
h3 { font-size: 12.5pt; color: #16324f; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 10.5pt; }
th, td { border: 1px solid #b9cde3; padding: 6px 9px; text-align: left; vertical-align: top; }
th { background: #e8f1fb; color: #0b5cab; }
code { background: #f0f4f9; padding: 1px 5px; border-radius: 4px; font-size: 10pt;
       font-family: Consolas, monospace; }
pre { background: #10233a; color: #dce9f7; padding: 12px 14px; border-radius: 8px;
      font-size: 9.5pt; overflow-x: hidden; white-space: pre-wrap; }
pre code { background: none; color: inherit; padding: 0; }
blockquote { border-left: 4px solid #0b5cab; background: #f2f7fd; margin: 12px 0;
             padding: 8px 14px; border-radius: 0 8px 8px 0; }
img { max-width: 100%; margin: 12px auto; display: block; }
a { color: #0b5cab; }
.module { page-break-before: always; }
.cover { page-break-after: always; text-align: center; padding-top: 220px; }
.cover h1 { border: none; font-size: 34pt; }
.cover .sub { font-size: 15pt; color: #5b6b7b; margin-top: 8px; }
.cover .meta { margin-top: 60px; color: #5b6b7b; font-size: 11pt; }
.toc { page-break-after: always; }
.toc li { margin: 7px 0; font-size: 12.5pt; }
.footer-note { color: #8296aa; font-size: 9pt; margin-top: 40px; }
"""

COVER = """
<div class="cover">
  <h1>AI-901<br/>Introduction to AI in Azure</h1>
  <div class="sub">Complete Course &mdash; Study Notes, Diagrams &amp; Exam Preparation</div>
  <div class="meta">
    Faculty Study Kit &middot; Original content authored from public Microsoft Learn documentation<br/>
    Exam weights: Identify AI concepts &amp; capabilities (~40%) &middot;
    Implement AI solutions with Microsoft Foundry (~60%)
  </div>
</div>
"""

files = sorted(glob.glob(os.path.join(MODULES, "*.md")))
md = markdown.Markdown(extensions=["tables", "fenced_code"])

toc_items, bodies = [], []
for f in files:
    with open(f, encoding="utf-8") as fh:
        text = fh.read()
    title = re.match(r"#\s*(.+)", text).group(1)
    anchor = os.path.basename(f)[:2]
    toc_items.append(f'<li><a href="#m{anchor}">{title}</a></li>')
    # inline the SVG diagrams so the PDF is self-contained
    def inline_img(m):
        path = os.path.join(DIAGRAMS, os.path.basename(m.group(1)))
        with open(path, encoding="utf-8") as sf:
            svg = sf.read()
        return svg
    text = re.sub(r"!\[[^\]]*\]\((\.\./diagrams/[^)]+)\)", inline_img, text)
    # drop the "Next:" nav lines (meaningless in a PDF)
    text = re.sub(r"\*\*(Next|Back to).*$", "", text, flags=re.M | re.S)
    html_body = md.reset().convert(text)
    bodies.append(f'<div class="module" id="m{anchor}">{html_body}</div>')

toc = ('<div class="toc"><h1>Contents</h1><ol>' + "".join(toc_items) +
       "</ol><p class='footer-note'>All diagrams and text in this document are original "
       "works created for this study kit. No Microsoft courseware material is reproduced. "
       "Official learning content: https://aka.ms/mslearn-ai-901</p></div>")

html_doc = (f"<!doctype html><html><head><meta charset='utf-8'>"
            f"<title>AI-901 Complete Course</title><style>{CSS}</style></head>"
            f"<body>{COVER}{toc}{''.join(bodies)}</body></html>")

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_doc)
print("wrote", OUT_HTML)

subprocess.run([EDGE, "--headless", "--disable-gpu",
                f"--print-to-pdf={OUT_PDF}", "--no-pdf-header-footer",
                "file:///" + OUT_HTML.replace("\\", "/")],
               check=True, capture_output=True, timeout=120)
print("wrote", OUT_PDF)
