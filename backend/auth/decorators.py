from functools import wraps
from flask import request, jsonify
import jwt
import os
SECRET_KEY = os.environ.get("JWT_SECRET", "dev-secret-change-this")
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "token is missing"}), 401
        try:
            if token.startswith("Bearer "):
                token = token.split(" ")[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_email = data["email"]
        except Exception:
            return jsonify({"error": "token is invalid or expired"}), 401
        return f(*args, **kwargs)
    return decorated