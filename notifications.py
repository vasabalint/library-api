from utils.fine_calculator import money

"""
Notifications module.
Mocks the notification logic for the library system.
Reference: https://en.wikipedia.org/wiki/Mock_object

In a production system, sending notifications would involve an external
email service (e.g. SMTP server, SendGrid, Amazon SES). As defined in software
engineering, mock objects are simulated objects that mimic the behavior of real
objects in controlled ways. Here, we mock the notification logic by simulating
the mail server and writing formatted notifications to 'outbox.txt'.
"""

OUTBOX_FILE = "outbox.txt"


class MockNotificationService:
    """
    Mock object that simulates a real notification / email service.
    Instead of connecting to an external network service or SMTP server,
    it records outgoing notifications into an outbox file ('outbox.txt').
    """

    def __init__(self, outbox_file: str = OUTBOX_FILE):
        self.outbox_file = outbox_file

    def _write_outbox(self, to_email: str, subject: str, body: str) -> None:
        """Simulates sending an email by appending to the outbox file."""
        with open(self.outbox_file, "a") as f:
            f.write(f"TO: {to_email} | SUBJECT: {subject} | BODY: {body}\n")

    def notify_checkout(self, to_email: str, book_title: str) -> None:
        """Mock loan checkout notice."""
        self._write_outbox(to_email, "Book checked out", f"You checked out {book_title}")

    def notify_renew(self, to_email: str, book_title: str) -> None:
        """Mock loan renewal notice."""
        self._write_outbox(to_email, "Loan renewed", f"You renewed {book_title}")

    def notify_return(self, to_email: str, book_title: str, fine: float) -> None:
        """Mock return confirmation notice and fine statement."""
        self._write_outbox(
            to_email,
            "Book returned",
            f"You returned {book_title}. Fine: ${money(fine)}",
        )

    def notify_fine_paid(self, to_email: str, amount_paid: float) -> None:
        """Mock receipt notice for paid fine."""
        self._write_outbox(to_email, "Fine paid", f"We received ${money(amount_paid)}")


# Default mock instance for convenience
mock_notifier = MockNotificationService()


def notify_checkout(to_email: str, book_title: str) -> None:
    mock_notifier.notify_checkout(to_email, book_title)


def notify_renew(to_email: str, book_title: str) -> None:
    mock_notifier.notify_renew(to_email, book_title)


def notify_return(to_email: str, book_title: str, fine: float) -> None:
    mock_notifier.notify_return(to_email, book_title, fine)


def notify_fine_paid(to_email: str, amount_paid: float) -> None:
    mock_notifier.notify_fine_paid(to_email, amount_paid)
