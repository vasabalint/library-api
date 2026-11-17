"""
Rules facade module for backwards compatibility with existing tests.
Re-exports checks and fine calculation utilities.
"""
from utils.checks import (
    DEFAULT_LOAN_DAYS,
    LOAN_LIMITS,
    MAX_RENEWALS,
    RENEWAL_DAYS,
    check_book_available,
    check_loan_can_pay_fine,
    check_loan_can_renew,
    get_loan_limit,
)
from utils.fine_calculator import (
    DAILY_FINE_RATE,
    calculate_current_fine,
    calculate_days_late,
    calculate_fine_for_due_date,
    calculate_member_debt_and_open_loans,
    calculate_overdue_fine,
    money,
)

__all__ = [
    "DAILY_FINE_RATE",
    "DEFAULT_LOAN_DAYS",
    "RENEWAL_DAYS",
    "MAX_RENEWALS",
    "LOAN_LIMITS",
    "money",
    "get_loan_limit",
    "calculate_days_late",
    "calculate_overdue_fine",
    "calculate_fine_for_due_date",
    "calculate_current_fine",
    "calculate_member_debt_and_open_loans",
    "check_book_available",
    "check_loan_can_renew",
    "check_loan_can_pay_fine",
]
