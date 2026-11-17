from datetime import date, timedelta
from error_handling import AppError
from notifications import notify_checkout, notify_fine_paid, notify_renew, notify_return
from repositories import books as book_repo
from repositories import loans as loan_repo
from repositories import members as member_repo
from utils.checks import (
    DEFAULT_LOAN_DAYS,
    RENEWAL_DAYS,
    check_book_available,
    check_loan_can_pay_fine,
    check_loan_can_renew,
    get_loan_limit,
)
from utils.fine_calculator import (
    calculate_current_fine,
    calculate_days_late,
    calculate_fine_for_due_date,
    calculate_member_debt_and_open_loans,
    money,
)
from utils.validation import is_valid_date

"""
Loan Service module.
Orchestrates loan checkout, returns, renewals, fine payments, and notifications.
"""


def list_loans(overdue_filter: bool = False) -> list[dict]:
    """Retrieves all loans with calculated fines, optionally filtered by overdue status."""
    loans = loan_repo.list_loans()
    result = []
    for loan in loans:
        current_fine = calculate_current_fine(
            loan["due_date"],
            loan["returned"],
            loan["fine"],
        )
        days_late = calculate_days_late(loan["due_date"])
        if overdue_filter and (loan["returned"] or days_late <= 0):
            continue
        result.append({
            "id": loan["id"],
            "book_id": loan["book_id"],
            "member_id": loan["member_id"],
            "due_date": loan["due_date"],
            "returned": loan["returned"],
            "fine": money(loan["fine"]),
            "fine_paid": loan["fine_paid"],
            "renewals": loan["renewals"],
            "checked_out": loan["checked_out"],
            "current_fine": money(current_fine),
        })
    return result


def get_loan(loan_id: int) -> dict:
    """Finds a single loan by ID with current fine calculations."""
    loan = loan_repo.get_loan(loan_id)
    if loan is None:
        raise AppError("loan not found", 404)

    current_fine = calculate_current_fine(
        loan["due_date"],
        loan["returned"],
        loan["fine"],
    )
    return {
        "id": loan["id"],
        "book_id": loan["book_id"],
        "member_id": loan["member_id"],
        "due_date": loan["due_date"],
        "returned": loan["returned"],
        "fine": money(loan["fine"]),
        "fine_paid": loan["fine_paid"],
        "renewals": loan["renewals"],
        "checked_out": loan["checked_out"],
        "current_fine": money(current_fine),
    }


def create_loan(data: dict) -> dict:
    """Checks business constraints and creates a new book loan."""
    book_id = data.get("book_id")
    member_id = data.get("member_id")
    due_date_str = data.get("due_date")

    if not book_id or not member_id:
        raise AppError("book_id and member_id are required", 400)
    if due_date_str and not is_valid_date(due_date_str):
        raise AppError("invalid due_date", 400)

    book = book_repo.get_book(book_id)
    if book is None:
        raise AppError("book not found", 404)

    member = member_repo.get_member(member_id)
    if member is None:
        raise AppError("member not found", 404)

    if not check_book_available(book):
        raise AppError("book is not available", 409)

    member_loans = loan_repo.get_loans_by_member(member_id)
    owed, open_loans = calculate_member_debt_and_open_loans(member_loans)
    if owed > 0:
        raise AppError("member has unpaid fines", 409)

    limit = get_loan_limit(member["type"])
    if open_loans >= limit:
        raise AppError("loan limit reached", 409)

    today = date.today()
    due_date = due_date_str or (today + timedelta(days=DEFAULT_LOAN_DAYS)).isoformat()
    loan = loan_repo.create_loan(book_id, member_id, due_date, today.isoformat())

    # Simulated notification
    notify_checkout(member["email"], book["title"])

    return loan


def return_book(loan_id: int) -> dict:
    """Handles book return, fine calculation, and return notification."""
    loan = loan_repo.get_loan(loan_id)
    if loan is None:
        raise AppError("loan not found", 404)
    if loan["returned"]:
        raise AppError("loan already returned", 409)

    _, fine = calculate_fine_for_due_date(loan["due_date"])
    updated = loan_repo.return_loan(loan_id, loan["book_id"], fine)
    member = member_repo.get_member(loan["member_id"])
    book = book_repo.get_book(loan["book_id"])

    # Simulated notification
    notify_return(member["email"], book["title"], fine)

    return updated


def renew_loan(loan_id: int) -> dict:
    """Renews a loan for 14 additional days if not overdue or previously renewed."""
    loan = loan_repo.get_loan(loan_id)
    if loan is None:
        raise AppError("loan not found", 404)

    can_renew, error_msg = check_loan_can_renew(loan)
    if not can_renew:
        raise AppError(error_msg, 409)

    new_due = (date.fromisoformat(loan["due_date"]) + timedelta(days=RENEWAL_DAYS)).isoformat()
    updated = loan_repo.renew_loan(loan_id, new_due)
    member = member_repo.get_member(loan["member_id"])
    book = book_repo.get_book(loan["book_id"])

    # Simulated notification
    notify_renew(member["email"], book["title"])

    return updated


def pay_fine(loan_id: int) -> dict:
    """Records fine payment receipt after a book has been returned."""
    loan = loan_repo.get_loan(loan_id)
    if loan is None:
        raise AppError("loan not found", 404)

    can_pay, error_msg = check_loan_can_pay_fine(loan)
    if not can_pay:
        raise AppError(error_msg, 409)

    updated = loan_repo.pay_fine(loan_id)
    member = member_repo.get_member(loan["member_id"])

    # Simulated notification
    notify_fine_paid(member["email"], loan["fine"])

    return updated
