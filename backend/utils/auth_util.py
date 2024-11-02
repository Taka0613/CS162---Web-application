from flask import request, jsonify, current_app
from functools import wraps
import jwt


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get("authToken")
        if not token:
            return jsonify({"error": "Unauthorized"}), 401
        try:
            # Decode and verify the token using current_app's config
            jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Session expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)

    return decorated_function
