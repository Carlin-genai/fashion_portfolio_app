from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.portfolio import Portfolio
from models.work_item import WorkItem
from services.file_service import allowed_file, save_local
import os

work_item_bp = Blueprint("work_item", __name__)

@work_item_bp.route("/<portfolio_id>/work-items", methods=["POST"])
@jwt_required()
def upload_work_item(portfolio_id):
    uid = get_jwt_identity()
    p = Portfolio.query.get(portfolio_id)
    if not p: return jsonify({"msg":"portfolio not found"}),404
    if p.owner_id != uid: return jsonify({"msg":"forbidden"}),403

    if "file" not in request.files:
        return jsonify({"msg":"no file"}),400
    f = request.files["file"]
    if f.filename == "" or not allowed_file(f.filename):
        return jsonify({"msg":"invalid file"}),400

    saved = save_local(f, subfolder=portfolio_id)
    media_type = "image"
    fn = f.filename.lower()
    if fn.endswith((".mp4",".mov")): media_type="video"
    if fn.endswith(".pdf"): media_type="pdf"

    wi = WorkItem(portfolio_id=portfolio_id, title=request.form.get("title",""), description=request.form.get("description",""), media_url=saved, media_type=media_type, tags=request.form.get("tags",""), materials=request.form.get("materials",""))
    db.session.add(wi)
    db.session.commit()
    return jsonify({"msg":"uploaded","work_item_id":wi.id,"media_url":wi.media_url}),201

@work_item_bp.route("/<portfolio_id>/work-items", methods=["GET"])
@jwt_required()
def list_work_items(portfolio_id):
    p = Portfolio.query.get(portfolio_id)
    if not p: return jsonify({"msg":"portfolio not found"}),404
    items = [{"id":w.id,"title":w.title,"media_url":w.media_url,"media_type":w.media_type,"order":w.order} for w in p.work_items.order_by(WorkItem.order).all()]
    return jsonify(items)

@work_item_bp.route("/work-items/<work_item_id>", methods=["PUT"])
@jwt_required()
def update_work_item(work_item_id):
    wi = WorkItem.query.get(work_item_id)
    if not wi: return jsonify({"msg":"not found"}),404
    if wi.portfolio.owner_id != get_jwt_identity(): return jsonify({"msg":"forbidden"}),403
    data = request.json or {}
    wi.title = data.get("title", wi.title)
    wi.description = data.get("description", wi.description)
    wi.tags = data.get("tags", wi.tags)
    wi.materials = data.get("materials", wi.materials)
    if "order" in data:
        wi.order = int(data.get("order", wi.order))
    db.session.commit()
    return jsonify({"msg":"updated"})

@work_item_bp.route("/work-items/<work_item_id>", methods=["DELETE"])
@jwt_required()
def delete_work_item(work_item_id):
    wi = WorkItem.query.get(work_item_id)
    if not wi: return jsonify({"msg":"not found"}),404
    if wi.portfolio.owner_id != get_jwt_identity(): return jsonify({"msg":"forbidden"}),403
    # try remove local file
    try:
        if wi.media_url and os.path.exists(wi.media_url):
            os.remove(wi.media_url)
    except Exception:
        pass
    db.session.delete(wi)
    db.session.commit()
    return jsonify({"msg":"deleted"})

# Serve uploaded files (local storage)
@work_item_bp.route("/uploads/<path:filename>", methods=["GET"])
def serve_uploads(filename):
    uploads = current_app.config["UPLOAD_FOLDER"]
    return send_from_directory(uploads, filename, as_attachment=False)
