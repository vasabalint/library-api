import re
from datetime import date

"""
Validation utility module.
Handles input format and syntax validation (emails, ISBNs, dates, and member types).
"""


def is_valid_email(value) -> bool:
    """Validates basic email format."""
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", str(value)) is not None


def is_valid_isbn(value) -> bool:
    """Validates ISBN-10 or ISBN-13 format allowing hyphens."""
    digits = str(value).replace("-", "")
    return digits.isdigit() and len(digits) in (10, 13)


def is_valid_date(value) -> bool:
    """Validates ISO date format YYYY-MM-DD."""
    try:
        date.fromisoformat(str(value))
        return True
    except (ValueError, TypeError):
        return False


def is_valid_member_type(value) -> bool:
    """Validates member type is either student or staff."""
    return value in ("student", "staff")
