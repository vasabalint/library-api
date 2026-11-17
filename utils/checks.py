from datetime import date

"""
Checks utility module.
Handles business rule checks and domain constraints for loans, members, and books.
"""

DEFAULT_LOAN_DAYS = 14
RENEWAL_DAYS = 14
MAX_RENEWALS = 1

LOAN_LIMITS = {
    "student": 3,
    "staff": 5,
}


def get_loan_limit(member_type: str) -> int:
    """Returns borrowing limit based on member type (staff vs student)."""
    return LOAN_LIMITS.get(member_type, 3)


def check_book_available(book: dict) -> bool:
    """Checks if a book is currently available for checkout."""
    if not book:
        return False
    return bool(book.get("available", False))


def check_loan_can_renew(loan: dict) -> tuple[bool, str | None]:
    """
    Checks if a loan can be renewed.
    Returns (True, None) if allowed, or (False, error_message).
    """
    if loan.get("returned"):
        return False, "loan already returned"
    if date.fromisoformat(loan["due_date"]) < date.today():
        return False, "overdue loans cannot be renewed"
    if loan.get("renewals", 0) >= MAX_RENEWALS:
        return False, "loan was already renewed"
    return True, None


def check_loan_can_pay_fine(loan: dict) -> tuple[bool, str | None]:
    """
    Checks if fine for a loan can be paid.
    Returns (True, None) if allowed, or (False, error_message).
    """
    if not loan.get("returned"):
        return False, "return the book before paying"
    if loan.get("fine", 0) <= 0 or loan.get("fine_paid"):
        return False, "no fine to pay"
    return True, None
