from flask import jsonify

"""
Error handling module.
Provides centralized error response generation and custom exception handling.
"""


class AppError(Exception):
    """
    Custom application exception that carries a user-friendly error message
    and an HTTP status code.
    """

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def error_response(message: str, status_code: int):
    """
    Constructs a standardized JSON error response.
    Accepts a custom message and an HTTP status code.
    """
    return jsonify({"error": message}), status_code
