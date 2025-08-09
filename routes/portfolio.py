from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.portfolio import Portfolio
from models.work_item import WorkItem

portfolio_bp = Blueprint("portfolio", __name__)

@portfolio_bp.route("", methods=["POST"])
@jwt_required()
def create_portfolio():
    uid = get_jwt_identity()
    data = request.json or {}
    p = Portfolio(title=data.get("title","Untitled"), description=data.get("description",""), theme=data.get("theme","minimal"), owner_id=uid)
    db.session.add(p)
    db.session.commit()
    return jsonify({"msg":"created","portfolio_id":p.id}), 201

@portfolio_bp.route("", methods=["GET"])
@jwt_required()
def list_portfolios():
    uid = get_jwt_identity()
    ps = Portfolio.query.filter_by(owner_id=uid).all()
    out = [{"id":p.id,"title":p.title,"description":p.description,"theme":p.theme,"updated_at":p.updated_at.isoformat()} for p in ps]
    return jsonify(out)

@portfolio_bp.route("/<portfolio_id>", methods=["GET"])
@jwt_required()
def get_portfolio(portfolio_id):
    p = Portfolio.query.get(portfolio_id)
    if not p: return jsonify({"msg":"not found"}),404
    items = [{"id":w.id,"title":w.title,"media_url":w.media_url,"media_type":w.media_type,"order":w.order} for w in p.work_items.order_by(WorkItem.order).all()]
    return jsonify({"id":p.id,"title":p.title,"description":p.description,"theme":p.theme,"work_items":items})

@portfolio_bp.route("/<portfolio_id>", methods=["PUT"])
@jwt_required()
def update_portfolio(portfolio_id):
    uid = get_jwt_identity()
    p = Portfolio.query.get(portfolio_id)
    if not p: return jsonify({"msg":"not found"}),404
    if p.owner_id != uid: return jsonify({"msg":"forbidden"}),403
    data = request.json or {}
    p.title = data.get("title", p.title)
    p.description = data.get("description", p.description)
    p.theme = data.get("theme", p.theme)
    db.session.commit()
    return jsonify({"msg":"updated"})

@portfolio_bp.route("/<portfolio_id>", methods=["DELETE"])
@jwt_required()
def delete_portfolio(portfolio_id):
    uid = get_jwt_identity()
    p = Portfolio.query.get(portfolio_id)
    if not p: return jsonify({"msg":"not found"}),404
    if p.owner_id != uid: return jsonify({"msg":"forbidden"}),403
    db.session.delete(p)
    db.session.commit()
    return jsonify({"msg":"deleted"})
