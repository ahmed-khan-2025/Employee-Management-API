from flask import Blueprint, jsonify

from sqlalchemy import text

from .database import get_db


health_router = Blueprint(
    "health",
    __name__
)


@health_router.get("/health")
def health():

    return jsonify({
        "status": "healthy"
    }), 200


@health_router.get("/health/db")
def database_health():

    db = get_db()

    try:

        db.execute(text("SELECT 1"))

        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200

    except Exception:

        return jsonify({
            "status": "unhealthy",
            "database": "disconnected"
        }), 503

    finally:

        db.close()