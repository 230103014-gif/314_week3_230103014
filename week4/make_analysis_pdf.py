from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer
)

source = Path("analysis.md").read_text(encoding="utf-8")
styles = getSampleStyleSheet()
styles["Normal"].fontSize = 10
styles["Normal"].leading = 15
styles["Heading2"].spaceBefore = 16

story = []

for block in source.split("\n\n"):
    block = block.strip()
    if not block:
        continue

    if block.startswith("# "):
        style = styles["Title"]
        block = block[2:]
    elif block.startswith("## "):
        style = styles["Heading2"]
        block = block[3:]
    else:
        style = styles["Normal"]

    # Standard PDF fonts may not support these symbols.
    block = block.replace("×", "x").replace("−", "-").replace("–", "-")
    block = escape(block).replace("\n", "<br/>").replace("`", "")
    story.append(Paragraph(block, style))
    story.append(Spacer(1, 8))

def page_number(canvas, document):
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(560, 35, f"Page {document.page}")

pdf = SimpleDocTemplate(
    "analysis.pdf",
    pagesize=letter,
    rightMargin=50,
    leftMargin=50,
    topMargin=45,
    bottomMargin=50,
)
pdf.build(story, onFirstPage=page_number, onLaterPages=page_number)
print("Saved analysis.pdf")