import unittest
from datetime import date
from rules import (
    DAILY_FINE_RATE,
    calculate_current_fine,
    calculate_days_late,
    calculate_fine_for_due_date,
    calculate_member_debt_and_open_loans,
    calculate_overdue_fine,
    get_loan_limit,
    money,
)


class DomainRulesTest(unittest.TestCase):
    def test_fine_rate_constant(self):
        self.assertEqual(DAILY_FINE_RATE, 0.50)

    def test_calculate_overdue_fine_without_db_or_http(self):
        self.assertEqual(calculate_overdue_fine(0), 0.0)
        self.assertEqual(calculate_overdue_fine(-3), 0.0)
        self.assertEqual(calculate_overdue_fine(1), 0.50)
        self.assertEqual(calculate_overdue_fine(5), 2.50)
        self.assertEqual(calculate_overdue_fine(10), 5.00)

    def test_calculate_fine_for_due_date(self):
        as_of = date(2026, 11, 10)
        days_late, fine = calculate_fine_for_due_date("2026-11-05", as_of_date=as_of)
        self.assertEqual(days_late, 5)
        self.assertEqual(fine, 2.50)

    def test_calculate_current_fine(self):
        as_of = date(2026, 11, 10)
        # Returned loan with stored fine of 2.0
        self.assertEqual(calculate_current_fine("2026-11-05", returned=True, stored_fine=2.0, as_of_date=as_of), 2.0)
        # Unreturned loan 5 days late
        self.assertEqual(calculate_current_fine("2026-11-05", returned=False, stored_fine=0.0, as_of_date=as_of), 2.50)
        # Unreturned loan not yet overdue
        self.assertEqual(calculate_current_fine("2026-11-15", returned=False, stored_fine=0.0, as_of_date=as_of), 0.0)

    def test_loan_limits(self):
        self.assertEqual(get_loan_limit("student"), 3)
        self.assertEqual(get_loan_limit("staff"), 5)
        self.assertEqual(get_loan_limit("unknown"), 3)

    def test_member_debt_calculation(self):
        as_of = date(2026, 11, 10)
        loans = [
            {"due_date": "2026-11-05", "returned": False, "fine": 0.0, "fine_paid": False},  # 5 days late -> 2.5
            {"due_date": "2026-11-01", "returned": True, "fine": 3.0, "fine_paid": False},   # returned unpaid fine -> 3.0
            {"due_date": "2026-10-20", "returned": True, "fine": 4.0, "fine_paid": True},    # returned paid fine -> 0.0
        ]
        total_owed, open_loans = calculate_member_debt_and_open_loans(loans, as_of_date=as_of)
        self.assertEqual(total_owed, 5.5)
        self.assertEqual(open_loans, 1)


if __name__ == "__main__":
    unittest.main()
