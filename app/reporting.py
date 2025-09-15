from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io

def build_pdf_report(summary: dict) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    width, height = letter
    y = height - 0.75*inch

    c.setFont("Helvetica-Bold", 16)
    c.drawString(0.75*inch, y, "ClearPoint Data Health Report")
    y -= 24
    c.setFont("Helvetica", 11)
    for k, v in summary.items():
        line = f"{k}: {v}"
        if y < 1*inch:
            c.showPage(); y = height - 0.75*inch; c.setFont("Helvetica", 11)
        c.drawString(0.75*inch, y, line); y -= 16
    c.showPage()
    c.save()
    buf.seek(0)
    return buf.read()
