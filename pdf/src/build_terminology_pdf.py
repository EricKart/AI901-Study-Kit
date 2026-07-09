"""Build the AI-901 Exam Terminology & Concepts Reference PDF.

Run:  python build_terminology_pdf.py
"""
import os
import subprocess

import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(HERE, "terminology.md")
OUT_HTML = os.path.join(HERE, "terminology.html")
OUT_PDF = os.path.join(ROOT, "pdf", "AI-901-Exam-Terminology-Reference.pdf")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

CSS = """
@page { size: A4; margin: 18mm 16mm; }
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', Arial, sans-serif; color: #16324f; font-size: 11.5pt;
       line-height: 1.55; margin: 0; }
h1 { font-size: 21pt; color: #0b5cab; border-bottom: 3px solid #0b5cab;
     padding-bottom: 6px; margin: 0 0 12px; }
h2 { font-size: 14.5pt; color: #0b5cab; margin: 26px 0 8px; page-break-after: avoid; }
h3 { font-size: 12.5pt; color: #16324f; page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 10.5pt;
        page-break-inside: avoid; }
th, td { border: 1px solid #b9cde3; padding: 6px 9px; text-align: left; vertical-align: top; }
th { background: #e8f1fb; color: #0b5cab; }
code { background: #f0f4f9; padding: 1px 5px; border-radius: 4px; font-size: 10pt;
       font-family: Consolas, monospace; }
blockquote { border-left: 4px solid #0b5cab; background: #f2f7fd; margin: 12px 0;
             padding: 8px 14px; border-radius: 0 8px 8px 0; page-break-inside: avoid; }
hr { border: 0; border-top: 1.5px solid #d5e2ef; margin: 22px 0; }
a { color: #0b5cab; }
em { color: #5b6b7b; }
.cover { page-break-after: always; text-align: center; padding-top: 230px; }
.cover h1 { border: none; font-size: 30pt; }
.cover .sub { font-size: 14pt; color: #5b6b7b; margin-top: 10px; }
.cover .meta { margin-top: 60px; color: #5b6b7b; font-size: 11pt; line-height: 1.8; }
"""

COVER = """
<div class="cover">
  <h1>AI-901<br/>Exam Terminology &amp; Concepts Reference</h1>
  <div class="sub">Section-wise glossary companion for the mock tests and the real exam</div>
  <div class="meta">
    Study this before attempting any timed test.<br/>
    Definitions, contrasts, and classic exam traps — no test questions or answers inside.<br/>
    Faculty Study Kit &middot; original content from public Microsoft Learn documentation
  </div>
</div>
"""

with open(SRC, encoding="utf-8") as f:
    text = f.read()
# the cover already carries the title — drop the markdown H1 to avoid duplication
text = text.split("\n", 1)[1]

md = markdown.Markdown(extensions=["tables", "fenced_code"])
body = md.convert(text)

html_doc = (f"<!doctype html><html><head><meta charset='utf-8'>"
            f"<title>AI-901 Exam Terminology Reference</title><style>{CSS}</style></head>"
            f"<body>{COVER}{body}</body></html>")

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_doc)
print("wrote", OUT_HTML)

subprocess.run([EDGE, "--headless", "--disable-gpu",
                f"--print-to-pdf={OUT_PDF}", "--no-pdf-header-footer",
                "file:///" + OUT_HTML.replace("\\", "/")],
               check=True, capture_output=True, timeout=120)
print("wrote", OUT_PDF)
