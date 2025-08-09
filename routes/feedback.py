from flask import Blueprint, request, jsonify
from extensions import db
from models.feedback import Feedback

feedback_bp = Blueprint("feedback", __name__)

@feedback_bp.route("", methods=["POST"])
def post_feedback():
    data = request.json or {}
    fb = Feedback(portfolio_id=data.get("portfolio_id"), author_id=data.get("author_id"), strong_points=data.get("strong_points",""), areas_to_improve=data.get("areas_to_improve",""), market_suggestions=data.get("market_suggestions",""), rating=int(data.get("rating",0)) if data.get("rating") else None)
    db.session.add(fb)
    db.session.commit()
    return jsonify({"msg":"feedback created","id":fb.id}),201

@feedback_bp.route("/<portfolio_id>", methods=["GET"])
def get_feedback_for_portfolio(portfolio_id):
    list_fb = Feedback.query.filter_by(portfolio_id=portfolio_id).order_by(Feedback.created_at.desc()).all()
    out = [{"id":f.id,"author_id":f.author_id,"strong_points":f.strong_points,"areas_to_improve":f.areas_to_improve,"market_suggestions":f.market_suggestions,"rating":f.rating,"created_at":f.created_at.isoformat()} for f in list_fb]
    return jsonify(out)
