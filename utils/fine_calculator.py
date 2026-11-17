from datetime import date

"""
Fine calculation utility module.
Calculates overdue days, daily fine rates, and outstanding member debts.
"""

DAILY_FINE_RATE = 0.50


def money(value) -> float:
    """Rounds monetary value to 2 decimal places."""
    return round(float(value), 2)


def calculate_days_late(due_date_str: str, as_of_date: date | None = None) -> int:
    """Calculates days late relative to given date (defaults to today)."""
    if as_of_date is None:
        as_of_date = date.today()
    due_date = date.fromisoformat(due_date_str)
    return (as_of_date - due_date).days


def calculate_overdue_fine(days_late: int) -> float:
    """Calculates fine for a given number of days late using standard daily rate."""
    return max(0, days_late) * DAILY_FINE_RATE


def calculate_fine_for_due_date(due_date_str: str, as_of_date: date | None = None) -> tuple[int, float]:
    """Returns (days_late, fine) for a due date."""
    days_late = calculate_days_late(due_date_str, as_of_date)
    return days_late, calculate_overdue_fine(days_late)


def calculate_current_fine(
    due_date_str: str,
    returned: bool,
    stored_fine: float = 0.0,
    as_of_date: date | None = None,
) -> float:
    """Determines active fine: stored fine if returned, or accrued overdue fine if open."""
    if returned:
        return stored_fine
    return calculate_overdue_fine(calculate_days_late(due_date_str, as_of_date))


def calculate_member_debt_and_open_loans(
    loans_records,
    as_of_date: date | None = None,
) -> tuple[float, int]:
    """Computes total unpaid debt and count of open loans for a member."""
    owed = 0.0
    open_loans = 0
    for loan in loans_records:
        returned = bool(loan["returned"] if isinstance(loan, dict) else loan[4])
        due_date_str = loan["due_date"] if isinstance(loan, dict) else loan[3]
        fine = loan["fine"] if isinstance(loan, dict) else loan[5]
        fine_paid = bool(loan["fine_paid"] if isinstance(loan, dict) else loan[6])

        if not returned:
            open_loans += 1
            days_late = calculate_days_late(due_date_str, as_of_date)
            if days_late > 0:
                owed += calculate_overdue_fine(days_late)
        elif not fine_paid:
            owed += fine
    return money(owed), open_loans
