from repositories import loans as loan_repo
from repositories import reports as report_repo
from utils.fine_calculator import calculate_days_late, calculate_overdue_fine, money

"""
Report Service module.
Handles data aggregation for overdue reports and library metrics summaries.
"""


def get_overdue_report() -> dict:
    """Aggregates all unreturned overdue loans and total outstanding fines."""
    rows = report_repo.get_unreturned_loans_with_details()
    items = []
    total = 0.0
    for r in rows:
        days_late = calculate_days_late(r["due_date"])
        if days_late > 0:
            fine = calculate_overdue_fine(days_late)
            total += fine
            items.append({
                "loan_id": r["loan_id"],
                "title": r["title"],
                "member": r["member"],
                "days_late": days_late,
                "fine": money(fine),
            })
    return {"items": items, "total_fines": money(total)}


def get_summary_report() -> dict:
    """Calculates overall catalog count, active loans, and total unpaid fines."""
    total_books = report_repo.get_total_books_count()
    loans = loan_repo.list_loans()
    on_loan = 0
    outstanding = 0.0
    for loan in loans:
        if not loan["returned"]:
            on_loan += 1
            days_late = calculate_days_late(loan["due_date"])
            outstanding += calculate_overdue_fine(days_late)
        elif not loan["fine_paid"]:
            outstanding += loan["fine"]
    return {
        "total_books": total_books,
        "on_loan": on_loan,
        "fines_outstanding": money(outstanding),
    }
