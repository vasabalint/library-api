import os
import unittest
from notifications import MockNotificationService


class MockNotificationsTest(unittest.TestCase):
    def setUp(self):
        self.test_outbox = "test_outbox.txt"
        if os.path.exists(self.test_outbox):
            os.remove(self.test_outbox)
        self.mock_service = MockNotificationService(outbox_file=self.test_outbox)

    def tearDown(self):
        if os.path.exists(self.test_outbox):
            os.remove(self.test_outbox)

    def test_notify_checkout(self):
        self.mock_service.notify_checkout("student@ada.edu.az", "Clean Code")
        with open(self.test_outbox) as f:
            content = f.read()
        self.assertIn("TO: student@ada.edu.az", content)
        self.assertIn("SUBJECT: Book checked out", content)
        self.assertIn("BODY: You checked out Clean Code", content)

    def test_notify_renew(self):
        self.mock_service.notify_renew("student@ada.edu.az", "Design Patterns")
        with open(self.test_outbox) as f:
            content = f.read()
        self.assertIn("SUBJECT: Loan renewed", content)
        self.assertIn("BODY: You renewed Design Patterns", content)

    def test_notify_return(self):
        self.mock_service.notify_return("student@ada.edu.az", "Refactoring", 1.50)
        with open(self.test_outbox) as f:
            content = f.read()
        self.assertIn("SUBJECT: Book returned", content)
        self.assertIn("Fine: $1.5", content)

    def test_notify_fine_paid(self):
        self.mock_service.notify_fine_paid("student@ada.edu.az", 3.00)
        with open(self.test_outbox) as f:
            content = f.read()
        self.assertIn("SUBJECT: Fine paid", content)
        self.assertIn("We received $3.0", content)


if __name__ == "__main__":
    unittest.main()
