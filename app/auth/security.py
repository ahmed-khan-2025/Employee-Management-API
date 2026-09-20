from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt

from flask import (
    current_app,
    jsonify,
    request,
    redirect,
    url_for,
    session
)


# =========================================================
# CREATE JWT ACCESS TOKEN
# =========================================================

def create_access_token(user_id, username, role):

    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "username": username,
        "role": role,
        "iat": now,
        "exp": now + timedelta(hours=1)
    }

    return jwt.encode(
        payload,
        current_app.config["JWT_SECRET_KEY"],
        algorithm="HS256"
    )


# =========================================================
# DECODE JWT TOKEN
# =========================================================

def decode_token(token):

    return jwt.decode(
        token,
        current_app.config["JWT_SECRET_KEY"],
        algorithms=["HS256"]
    )


# =========================================================
# GET BEARER TOKEN FROM REQUEST
# =========================================================

def get_token():

    auth_header = request.headers.get(
        "Authorization"
    )

    if not auth_header:
        return None

    parts = auth_header.split()

    if len(parts) != 2:
        return None

    if parts[0].lower() != "bearer":
        return None

    return parts[1]


# =========================================================
# JWT REQUIRED
# =========================================================

def jwt_required():

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            token = get_token()

            if not token:

                return jsonify({
                    "error": "Unauthorized",
                    "message": "Bearer token is required"
                }), 401

            try:

                payload = decode_token(
                    token
                )

            except jwt.ExpiredSignatureError:

                return jsonify({
                    "error": "Unauthorized",
                    "message": "Token has expired"
                }), 401

            except jwt.InvalidTokenError:

                return jsonify({
                    "error": "Unauthorized",
                    "message": "Invalid token"
                }), 401

            request.current_user = payload

            return function(
                *args,
                **kwargs
            )

        return wrapper

    return decorator


# =========================================================
# ROLE REQUIRED
# =========================================================

def role_required(*allowed_roles):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            token = get_token()

            if not token:

                return jsonify({
                    "error": "Unauthorized",
                    "message": "Bearer token is required"
                }), 401

            try:

                payload = decode_token(
                    token
                )

            except jwt.ExpiredSignatureError:

                return jsonify({
                    "error": "Unauthorized",
                    "message": "Token has expired"
                }), 401

            except jwt.InvalidTokenError:

                return jsonify({
                    "error": "Unauthorized",
                    "message": "Invalid token"
                }), 401

            role = payload.get(
                "role"
            )

            if role not in allowed_roles:

                return jsonify({
                    "error": "Forbidden",
                    "message": "Insufficient permissions"
                }), 403

            request.current_user = payload

            return function(
                *args,
                **kwargs
            )

        return wrapper

    return decorator


# =========================================================
# WEB LOGIN REQUIRED
# =========================================================

def web_login_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        # Check whether the user has logged in
        if "access_token" not in session:

            return redirect(
                url_for(
                    "auth.web_login_page"
                )
            )

        return function(
            *args,
            **kwargs
        )

    return wrapper