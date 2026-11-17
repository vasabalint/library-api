from error_handling import AppError
from repositories import books as book_repo
from utils.checks import check_book_available
from utils.validation import is_valid_isbn

"""
Book Service module.
Handles business logic for book management, validation, and availability rules.
"""


def list_books(available_only: bool = False) -> list[dict]:
    """Retrieves books, optionally filtered by availability."""
    return book_repo.list_books(available_only=available_only)


def get_book(book_id: int) -> dict:
    """Retrieves a single book by ID, raising 404 if not found."""
    book = book_repo.get_book(book_id)
    if book is None:
        raise AppError("book not found", 404)
    return book


def create_book(data: dict) -> dict:
    """Validates book details and creates a new book record."""
    title = data.get("title")
    author = data.get("author")
    isbn = data.get("isbn")

    if not title or not author:
        raise AppError("title and author are required", 400)
    if not is_valid_isbn(isbn):
        raise AppError("invalid isbn", 400)

    return book_repo.create_book(title, author, isbn)


def delete_book(book_id: int) -> None:
    """Deletes a book if it exists and is not currently loaned out."""
    book = get_book(book_id)
    if not check_book_available(book):
        raise AppError("book is on loan", 409)
    book_repo.delete_book(book_id)
