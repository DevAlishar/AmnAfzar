from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from app import create_app
from flask import render_template

users_bp = Blueprint("users", __name__)
@users_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@users_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")
@users_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered."}), 400

    password_hash = generate_password_hash(password)
    new_user = User(email=email, password_hash=password_hash)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully."}), 201

@users_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials."}), 401

    token = jwt.encode({"id": user.id, "exp": datetime.utcnow() + timedelta(hours=1)}, 
    create_app().config["SECRET_KEY"], algorithm="HS256")
    return jsonify({"access_token": token}), 200