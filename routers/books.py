from flask import Blueprint, jsonify, request
from error_handling import AppError, error_response
from services import books as book_service

books_bp = Blueprint("books", __name__)


@books_bp.route("/books", methods=["GET"])
def list_books():
    available_only = request.args.get("available") == "true"
    books = book_service.list_books(available_only=available_only)
    return jsonify(books)


@books_bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    try:
        book = book_service.get_book(book_id)
        return jsonify(book)
    except AppError as e:
        return error_response(e.message, e.status_code)


@books_bp.route("/books", methods=["POST"])
def create_book():
    data = request.get_json(silent=True) or {}
    try:
        book = book_service.create_book(data)
        return jsonify(book), 201
    except AppError as e:
        return error_response(e.message, e.status_code)


@books_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    try:
        book_service.delete_book(book_id)
        return "", 204
    except AppError as e:
        return error_response(e.message, e.status_code)
