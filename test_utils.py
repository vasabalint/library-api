import unittest
from datetime import date
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
from utils.validation import (
    is_valid_date,
    is_valid_email,
    is_valid_isbn,
    is_valid_member_type,
)


class ValidationUtilsTest(unittest.TestCase):
    def test_email_validation(self):
        self.assertTrue(is_valid_email("student@ada.edu.az"))
        self.assertTrue(is_valid_email("user.name@example.com"))
        self.assertFalse(is_valid_email("not-an-email"))
        self.assertFalse(is_valid_email("missing-domain@"))
        self.assertFalse(is_valid_email("@missing-user.com"))

    def test_isbn_validation(self):
        self.assertTrue(is_valid_isbn("0-13-235088-2"))
        self.assertTrue(is_valid_isbn("978-0132350884"))
        self.assertFalse(is_valid_isbn("12345"))
        self.assertFalse(is_valid_isbn("invalid-isbn-xyz"))

    def test_date_validation(self):
        self.assertTrue(is_valid_date("2026-11-20"))
        self.assertFalse(is_valid_date("not-a-date"))
        self.assertFalse(is_valid_date("2026-13-45"))

    def test_member_type_validation(self):
        self.assertTrue(is_valid_member_type("student"))
        self.assertTrue(is_valid_member_type("staff"))
        self.assertFalse(is_valid_member_type("admin"))
        self.assertFalse(is_valid_member_type("guest"))


class ChecksUtilsTest(unittest.TestCase):
    def test_loan_limits(self):
        self.assertEqual(get_loan_limit("student"), 3)
        self.assertEqual(get_loan_limit("staff"), 5)
        self.assertEqual(get_loan_limit("other"), 3)

    def test_check_book_available(self):
        self.assertTrue(check_book_available({"id": 1, "available": True}))
        self.assertFalse(check_book_available({"id": 1, "available": False}))
        self.assertFalse(check_book_available(None))

    def test_check_loan_can_renew(self):
        # Returned loan cannot be renewed
        can_renew, err = check_loan_can_renew({"returned": True, "due_date": "2026-12-01", "renewals": 0})
        self.assertFalse(can_renew)
        self.assertEqual(err, "loan already returned")

        # Overdue loan cannot be renewed
        can_renew, err = check_loan_can_renew({"returned": False, "due_date": "2020-01-01", "renewals": 0})
        self.assertFalse(can_renew)
        self.assertEqual(err, "overdue loans cannot be renewed")

        # Already renewed loan cannot be renewed
        can_renew, err = check_loan_can_renew({"returned": False, "due_date": "2099-01-01", "renewals": 1})
        self.assertFalse(can_renew)
        self.assertEqual(err, "loan was already renewed")

        # Valid open loan can be renewed
        can_renew, err = check_loan_can_renew({"returned": False, "due_date": "2099-01-01", "renewals": 0})
        self.assertTrue(can_renew)
        self.assertIsNone(err)

    def test_check_loan_can_pay_fine(self):
        # Unreturned loan cannot pay fine
        can_pay, err = check_loan_can_pay_fine({"returned": False, "fine": 5.0, "fine_paid": False})
        self.assertFalse(can_pay)
        self.assertEqual(err, "return the book before paying")

        # No fine or already paid
        can_pay, err = check_loan_can_pay_fine({"returned": True, "fine": 0.0, "fine_paid": False})
        self.assertFalse(can_pay)
        self.assertEqual(err, "no fine to pay")

        can_pay, err = check_loan_can_pay_fine({"returned": True, "fine": 5.0, "fine_paid": True})
        self.assertFalse(can_pay)
        self.assertEqual(err, "no fine to pay")

        # Valid fine to pay
        can_pay, err = check_loan_can_pay_fine({"returned": True, "fine": 2.5, "fine_paid": False})
        self.assertTrue(can_pay)
        self.assertIsNone(err)


class FineCalculatorUtilsTest(unittest.TestCase):
    def test_money_rounding(self):
        self.assertEqual(money(2.5), 2.50)
        self.assertEqual(money(2.555), 2.56)

    def test_fine_calculations(self):
        self.assertEqual(calculate_overdue_fine(0), 0.0)
        self.assertEqual(calculate_overdue_fine(-2), 0.0)
        self.assertEqual(calculate_overdue_fine(4), 2.0)

    def test_as_of_due_date_fine(self):
        as_of = date(2026, 11, 10)
        days, fine = calculate_fine_for_due_date("2026-11-06", as_of_date=as_of)
        self.assertEqual(days, 4)
        self.assertEqual(fine, 2.0)


if __name__ == "__main__":
    unittest.main()
