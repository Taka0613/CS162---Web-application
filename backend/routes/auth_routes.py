from flask import Blueprint, request, jsonify, make_response, session
from app import db, bcrypt
from models import User
import jwt
import datetime

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    print(f"Received data: {data}")  # Debugging statement

    username = data.get("username")
    password = data.get("password")
    print(f"Username: {username}")  # Debugging statement
    print(f"Password: {password}")  # Debugging statement

    if not username or not password:
        print("Username or password is missing.")
        return jsonify({"message": "Username and password are required"}), 400

    existing_user = User.query.filter_by(username=username).first()
    print(f"Existing user: {existing_user}")  # Debugging statement

    if existing_user:
        print("Username already exists.")
        return jsonify({"message": "Username already exists"}), 409

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = User(username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    print("User registered successfully.")
    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Check if the user exists
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        # Generate a token (replace with your token generation logic)
        token = jwt.encode(
            {
                "user_id": user.user_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            },
            "YOUR_SECRET_KEY",
            algorithm="HS256",
        )

        # Create response and set cookie
        response = make_response(jsonify({"message": "Login successful"}))
        response.set_cookie(
            "authToken",
            token,  # The generated token
            httponly=True,  # Cookie is HTTP-only for security
            samesite="Lax",  # Lax for cross-site protection
        )
        return response

    return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out"}), 200
