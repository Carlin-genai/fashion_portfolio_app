from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.ai_service import analyze_portfolio
from models import Portfolio

ai_bp = Blueprint("ai", __name__, url_prefix="/ai")

@ai_bp.route("/analyze", methods=["POST"])
@jwt_required()
def analyze():
    """
    Accepts payload:
    {
      "portfolio_id": "pf_xxx"
    }
    Returns analysis JSON.
    """
    data = request.json or {}
    pid = data.get("portfolio_id")
    p = Portfolio.query.get(pid)
    if not p:
        return jsonify({"msg": "portfolio not found"}), 404
    # Build minimal portfolio data and work items
    work_items = []
    for wi in p.work_items:
        work_items.append({
            "id": wi.id,
            "title": wi.title,
            "description": wi.description,
            "media_type": wi.media_type,
            "media_url": wi.media_url,
            "tags": wi.tags,
            "materials": wi.materials
        })
    result = analyze_portfolio({
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "theme": p.theme
    }, work_items)
    return jsonify({"analysis": result})
