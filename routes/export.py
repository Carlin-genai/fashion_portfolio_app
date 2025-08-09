from flask import Blueprint, send_file, jsonify
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from models.portfolio import Portfolio
from models.work_item import WorkItem

export_bp = Blueprint("export", __name__)

@export_bp.route("/pdf/<portfolio_id>", methods=["GET"])
def export_pdf(portfolio_id):
    p = Portfolio.query.get(portfolio_id)
    if not p:
        return jsonify({"msg":"not found"}), 404

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 40
    y = height - margin

    c.setFont("Helvetica-Bold", 20)
    c.drawString(margin, y, p.title or "Portfolio")
    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(margin, y, p.description or "")
    y -= 40

    # one page per work item with text (images optional)
    for w in p.work_items:
        c.showPage()
        y = height - margin
        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin, y, w.title or "")
        y -= 24
        c.setFont("Helvetica", 11)
        c.drawString(margin, y, w.description or "")
    c.save()
    buffer.seek(0)
    return send_file(buffer, mimetype="application/pdf", as_attachment=True, download_name=f"{p.title or 'portfolio'}.pdf")
