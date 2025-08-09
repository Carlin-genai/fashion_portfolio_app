from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json or {}
    if not data.get("email") or not data.get("password"):
        return jsonify({"msg":"email & password required"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"msg":"email exists"}), 409
    u = User(email=data["email"], name=data.get("name"))
    u.set_password(data["password"])
    db.session.add(u)
    db.session.commit()
    token = create_access_token(identity=u.id)
    return jsonify({"access_token": token, "user": {"id": u.id, "email": u.email}}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    user = User.query.filter_by(email=data.get("email")).first()
    if not user or not user.check_password(data.get("password","")):
        return jsonify({"msg":"bad credentials"}), 401
    token = create_access_token(identity=user.id)
    return jsonify({"access_token": token, "user": {"id": user.id, "email": user.email}})
