import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key-for-employee-management-api-2026"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "dev-jwt-secret-key-for-employee-management-api-2026"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL"
    )

    DEBUG = (
        os.getenv(
            "FLASK_DEBUG",
            "false"
        ).lower()
        == "true"
    )