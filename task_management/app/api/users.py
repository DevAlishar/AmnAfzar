from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
import jwt
from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

users_bp = Blueprint("users", __name__)

@users_bp.route("/", methods=["GET"])
def get_users():
    """
    Get all users
    ---
    responses:
      200:
        description: A list of users
    """
    users = User.query.all()
    return jsonify([{"id": user.id, "email": user.email} for user in users]), 200

@users_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """
    Get a user by ID
    ---
    parameters:
      - name: user_id
        type: integer
        required: true
        description: ID of the user
    responses:
      200:
        description: User details
      404:
        description: User not found
    """
    user = User.query.get(user_id)
    if user:
        return jsonify({"id": user.id, "email": user.email}), 200
    return jsonify({"error": "User  not found"}), 404

@users_bp.route("/register", methods=["POST"])
def register():
    """
    User Registration
    ---
    parameters:
      - name: email
        type: string
        required: true
        description: User's email
      - name: password
        type: string
        required: true
        description: User's password
    responses:
      201:
        description: User registered successfully
      400:
        description: Email already registered or missing fields
    """
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

    return jsonify({"message": "User  registered successfully."}), 201

@users_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """
    Update a user by ID
    ---
    parameters:
      - name: user_id
        type: integer
        required: true
        description: ID of the user
      - name: email
        type: string
        required: false
        description: New email of the user
    responses:
      200:
        description: User updated successfully
      404:
        description: User not found
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User  not found"}), 404

    data = request.json
    user.email = data.get("email", user.email)

    db.session.commit()
    return jsonify({"message": "User  updated successfully."}), 200

@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete a user by ID
    ---
    parameters:
      - name: user_id
        type: integer
        required: true
        description: ID of the user
    responses:
      204:
        description: User deleted successfully
      404:
        description: User not found
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User  not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User  deleted successfully."}), 204
@users_bp.route("/login", methods=["POST"])
def login():
    """
    User Login
    ---
    parameters:
      - name: email
        type: string
        required: true
        description: User's email
      - name: password
        type: string
        required: true
        description: User's password
    responses:
      200:
        description: Login successful, returns access token
      401:
        description: Invalid credentials
    """
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials."}), 401

    token = jwt.encode({"id": user.id, "exp": datetime.utcnow() + timedelta(hours=1)}, 
    create_app().config["SECRET_KEY"], algorithm="HS256")
    return jsonify({"access_token": token}), 200