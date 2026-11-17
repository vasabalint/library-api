from error_handling import AppError
from repositories import loans as loan_repo
from repositories import members as member_repo
from utils.checks import get_loan_limit
from utils.fine_calculator import calculate_member_debt_and_open_loans, money
from utils.validation import is_valid_email, is_valid_member_type

"""
Member Service module.
Handles business logic for member registration, lookup, and loan limits/debts.
"""


def list_members() -> list[dict]:
    """Returns all registered members."""
    return member_repo.list_members()


def get_member(member_id: int) -> dict:
    """Finds a member by ID, raising 404 if not found."""
    member = member_repo.get_member(member_id)
    if member is None:
        raise AppError("member not found", 404)
    return member


def create_member(data: dict) -> dict:
    """Validates and registers a new library member."""
    name = data.get("name")
    email = data.get("email")
    member_type = data.get("type", "student")

    if not name:
        raise AppError("name is required", 400)
    if not is_valid_email(email):
        raise AppError("invalid email", 400)
    if not is_valid_member_type(member_type):
        raise AppError("type must be student or staff", 400)

    existing = member_repo.get_member_by_email(email)
    if existing is not None:
        raise AppError("email already registered", 409)

    return member_repo.create_member(name, email, member_type)


def get_member_loans(member_id: int) -> dict:
    """Returns loan history, total debt, and remaining loan quota for a member."""
    member = get_member(member_id)
    loans_list = loan_repo.get_loans_by_member(member_id)
    total_owed, open_loans = calculate_member_debt_and_open_loans(loans_list)

    formatted_loans = [
        {
            "id": l["id"],
            "book_id": l["book_id"],
            "due_date": l["due_date"],
            "returned": l["returned"],
            "fine": money(l["fine"]),
            "fine_paid": l["fine_paid"],
        }
        for l in loans_list
    ]

    limit = get_loan_limit(member["type"])
    remaining = limit - open_loans
    return {
        "loans": formatted_loans,
        "total_owed": total_owed,
        "loans_remaining": remaining,
    }
