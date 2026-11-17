import os
from flask import Flask
from database import init_db
from error_handling import AppError, error_response
from routers.books import books_bp
from routers.loans import loans_bp
from routers.members import members_bp
from routers.reports import reports_bp


def create_app() -> Flask:
    app = Flask(__name__)

    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        return error_response(error.message, error.status_code)

    app.register_blueprint(books_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(loans_bp)
    app.register_blueprint(reports_bp)

    return app


app = create_app()

if not os.path.exists("library.db"):
    init_db()

if __name__ == "__main__":
    app.run(port=8000)
