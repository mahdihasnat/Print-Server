from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

import io

def get_pdf(print):
	buffer = io.BytesIO()
	c = canvas.Canvas(buffer, pagesize=A4)
	# c.setFont("Monospaced", 12)
	c.drawString(inch, inch, print.source_code)
	c.save()
	buffer.seek(0)
	return buffer
