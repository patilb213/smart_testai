from flask import Blueprint, request, jsonify
import bcrypt
import jwt
import datetime
import os
from models.models import db, User
from utils.audit import write_audit_log

auth_bp = Blueprint("auth", __name__)
SECRET_KEY = os.environ.get("JWT_SECRET", "dev-secret-change-this")

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "name, email, and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already registered"}), 409

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(name=name, email=email, password_hash=hashed, role="tester")
    db.session.add(user)
    db.session.commit()

    write_audit_log(
        action="USER_SIGNUP", user=email, entity_type="User", entity_id=user.id,
        after_state={"name": name, "email": email}, ip_address=request.remote_addr
    )

    return jsonify({"message": "signup successful", "user_id": user.id}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        return jsonify({"error": "invalid email or password"}), 401

    token = jwt.encode(
        {"user_id": user.id, "email": user.email, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)},
        SECRET_KEY, algorithm="HS256"
    )

    write_audit_log(
        action="USER_LOGIN", user=email, entity_type="User", entity_id=user.id,
        ip_address=request.remote_addr
    )

    return jsonify({"message": "login successful", "token": token}), 200