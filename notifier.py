"""
Notifier compatibility facade.
Re-exports mock notification logic from notifications module.
Reference: https://en.wikipedia.org/wiki/Mock_object
"""
from notifications import (
    MockNotificationService,
    mock_notifier,
    notify_checkout,
    notify_fine_paid,
    notify_renew,
    notify_return,
)

__all__ = [
    "MockNotificationService",
    "mock_notifier",
    "notify_checkout",
    "notify_renew",
    "notify_return",
    "notify_fine_paid",
]
