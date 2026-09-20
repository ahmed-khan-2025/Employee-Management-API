from flask import (
    Flask,
    jsonify,
    request,
    render_template
)

from flasgger import Swagger

from werkzeug.exceptions import HTTPException

from .config import Config
from .logger import setup_logging
from .routers.employees import router
from .auth.routes import auth_router
from .health import health_router


# ---------------------------------------------------------
# APPLICATION
# ---------------------------------------------------------

app = Flask(__name__)

app.config.from_object(Config)


# ---------------------------------------------------------
# SWAGGER
# ---------------------------------------------------------

Swagger(app)


# ---------------------------------------------------------
# LOGGING
# ---------------------------------------------------------

logger = setup_logging()


# ---------------------------------------------------------
# REQUEST LOGGING
# ---------------------------------------------------------

@app.before_request
def log_request():

    logger.info(
        "Request: %s %s",
        request.method,
        request.path
    )


@app.after_request
def log_response(response):

    logger.info(
        "Response: %s %s -> %s",
        request.method,
        request.path,
        response.status_code
    )

    return response


# ---------------------------------------------------------
# BLUEPRINTS
# ---------------------------------------------------------

app.register_blueprint(
    router
)

app.register_blueprint(
    auth_router
)

app.register_blueprint(
    health_router
)


# ---------------------------------------------------------
# ROOT / DASHBOARD
# ---------------------------------------------------------

@app.get("/")
def home():

    return render_template(
        "index.html"
    )


# ---------------------------------------------------------
# WEB LOGIN PAGE
# ---------------------------------------------------------

@app.get("/login")
def login_page():

    return render_template(
        "login.html"
    )


# ---------------------------------------------------------
# HTTP ERROR HANDLER
# ---------------------------------------------------------

@app.errorhandler(HTTPException)
def handle_http_error(error):

    logger.warning(
        "HTTP error: %s %s - %s",
        error.code,
        error.name,
        error.description
    )

    return jsonify({
        "error": error.name,
        "message": error.description
    }), error.code


# ---------------------------------------------------------
# UNEXPECTED ERROR HANDLER
# ---------------------------------------------------------

@app.errorhandler(Exception)
def handle_unexpected_error(error):

    logger.exception(
        "Unexpected application error"
    )

    return jsonify({
        "error": "Internal server error"
    }), 500


# ---------------------------------------------------------
# APPLICATION START
# ---------------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=app.config["DEBUG"]
    )