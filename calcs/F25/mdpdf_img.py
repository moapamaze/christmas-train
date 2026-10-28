"""Render the calc-notes markdown to PDF (reportlab, DejaVu) with the PF-CT title footer."""
import sys, re
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("DV", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
src, out = sys.argv[1], sys.argv[2]
ss = getSampleStyleSheet()
body = ParagraphStyle("b", parent=ss["Normal"], fontName="DV", fontSize=8, leading=10)
cell = ParagraphStyle("c", parent=body, fontSize=6.5, leading=8)
h1 = ParagraphStyle("h1", parent=body, fontName="DVB", fontSize=14, leading=18, spaceAfter=6)
h2 = ParagraphStyle("h2", parent=body, fontName="DVB", fontSize=11, leading=14, spaceBefore=8, spaceAfter=4)
def esc(t): return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
flow, tbl = [], []
W = landscape(letter)[0] - 72
def flush():
    global tbl
    if not tbl: return
    rows = [r for r in tbl if not re.match(r"^\|[-| ]+\|$", r)]
    data = [[Paragraph(esc(c.strip()), cell) for c in r.strip().strip("|").split("|")] for r in rows]
    n = len(data[0]); t = Table(data, colWidths=[W / n] * n if n < 5 else None, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5e7eb")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    flow.append(t); flow.append(Spacer(1, 6)); tbl = []
for ln in open(src).read().split("\n"):
    if ln.startswith("|"): tbl.append(ln); continue
    flush()
    m = re.match(r"^!\[.*\]\((.+)\)$", ln)
    if m:
        im = Image(m.group(1)); s = min(W / im.drawWidth, 470 / im.drawHeight); im.drawWidth *= s; im.drawHeight *= s; flow.append(PageBreak()); flow.append(im); continue
    if ln.startswith("# "): flow.append(Paragraph(esc(ln[2:]), h1))
    elif ln.startswith("## "): flow.append(Paragraph(esc(ln[3:]), h2))
    elif ln.startswith("- "): flow.append(Paragraph("• " + esc(ln[2:]), body))
    elif ln.strip(): flow.append(Paragraph(esc(ln), body))
flush()
def foot(c, d):
    c.saveState(); c.setFont("DV", 7)
    c.drawString(36, 20, "Pulsipher Farms Christmas Train — preliminary, not for construction until PE stamped · PF-CT R2 · F25 drive options · 2026-10-27")
    c.drawRightString(landscape(letter)[0] - 36, 20, f"Page {d.page}"); c.restoreState()
SimpleDocTemplate(out, pagesize=landscape(letter), leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=40).build(flow, onFirstPage=foot, onLaterPages=foot)
