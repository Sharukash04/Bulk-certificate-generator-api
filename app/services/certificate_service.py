from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os


def generate_certificate(
    recipient_name:str,
    event_name:str,
    organization:str,
    certificate_id:int
):
    os.makedirs("generated",exist_ok=True)

    file_path=f"generated/certificate_{certificate_id}.pdf"

    pdf=canvas.Canvas(file_path,pagesize=A4)

    width,height=A4

    pdf.setTitle("Certificate")

    pdf.setFont("Helvetica-Bold",28)
    pdf.drawCentredString(
        width/2,
        height-70*mm,
        "CERTIFICATE OF PARTICIPATION"
    )

    pdf.setFont("Helvetica",16)
    pdf.drawCentredString(
        width/2,
        height-100*mm,
        "This certificate is proudly presented to"
    )

    pdf.setFont("Helvetica-Bold",24)
    pdf.drawCentredString(
        width/2,
        height-125*mm,
        recipient_name
    )

    pdf.setFont("Helvetica",15)
    pdf.drawCentredString(
        width/2,
        height-150*mm,
        f"For participating in {event_name}"
    )

    pdf.drawCentredString(
        width/2,
        height-170*mm,
        f"Organized by {organization}"
    )

    pdf.setFont("Helvetica",10)
    pdf.drawCentredString(
        width/2,
        30*mm,
        f"Certificate ID: {certificate_id}"
    )

    pdf.save()

    return file_path