from flask import (
    Blueprint,
    jsonify,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    session
)

from ..database import get_db
from ..services.auth_service import AuthService
from .security import jwt_required


auth_router = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


# =========================================================
# API - REGISTER
# =========================================================

@auth_router.post("/register")
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication

    consumes:
      - application/json

    parameters:
      - in: body
        name: user
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: admin123

    responses:
      201:
        description: User registered successfully

      400:
        description: Validation error

      409:
        description: Username already exists
    """

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Invalid request",
            "message": "JSON body is required"
        }), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Validation error",
            "message": "Username and password are required"
        }), 400

    db = get_db()

    try:
        service = AuthService(db)

        try:
            user = service.register(
                username,
                password
            )

        except ValueError as error:
            return jsonify({
                "error": "Conflict",
                "message": str(error)
            }), 409

        return jsonify({
            "id": user.id,
            "username": user.username,
            "role": user.role
        }), 201

    finally:
        db.close()


# =========================================================
# API - LOGIN
# =========================================================

@auth_router.post("/login")
def login():
    """
    Login and get JWT access token
    ---
    tags:
      - Authentication

    consumes:
      - application/json

    parameters:
      - in: body
        name: credentials
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: admin123

    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            access_token:
              type: string
              example: eyJhbGciOiJIUzI1NiIs...
            token_type:
              type: string
              example: Bearer

      400:
        description: Invalid request

      401:
        description: Invalid username or password
    """

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Invalid request",
            "message": "JSON body is required"
        }), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Validation error",
            "message": "Username and password are required"
        }), 400

    db = get_db()

    try:
        service = AuthService(db)

        try:
            user, token = service.authenticate(
                username,
                password
            )

        except ValueError as error:
            return jsonify({
                "error": "Unauthorized",
                "message": str(error)
            }), 401

        return jsonify({
            "access_token": token,
            "token_type": "Bearer"
        }), 200

    finally:
        db.close()


# =========================================================
# API - CURRENT USER
# =========================================================

@auth_router.get("/me")
@jwt_required()
def me():
    """
    Get current authenticated user
    ---
    tags:
      - Authentication

    security:
      - Bearer: []

    responses:
      200:
        description: Current user information

      401:
        description: Unauthorized
    """

    user = request.current_user

    return jsonify({
        "id": int(user["sub"]),
        "username": user["username"],
        "role": user["role"]
    }), 200


# =========================================================
# WEB - LOGIN PAGE
# =========================================================

@auth_router.get("/web-login")
def web_login_page():

    return render_template(
        "login.html"
    )


# =========================================================
# WEB - LOGIN
# =========================================================

@auth_router.post("/web-login")
def web_login():

    username = request.form.get(
        "username",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    )

    if not username or not password:
        flash(
            "Username and password are required."
        )

        return redirect(
            url_for("auth.web_login_page")
        )

    db = get_db()

    try:
        service = AuthService(db)

        try:
            user, token = service.authenticate(
                username,
                password
            )

        except ValueError:
            flash(
                "Invalid username or password."
            )

            return redirect(
                url_for("auth.web_login_page")
            )

        session["access_token"] = token
        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role

        flash(
            "Login successful."
        )

        return redirect(
            url_for("employees.employees_page")
        )

    finally:
        db.close()


# =========================================================
# WEB - LOGOUT
# =========================================================

@auth_router.get("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out."
    )

    return redirect(
        url_for("auth.web_login_page")
    )
