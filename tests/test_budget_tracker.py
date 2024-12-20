import pytest
from budget_tracker import BudgetTracker
from unittest.mock import MagicMock

@pytest.fixture
def tracker():
    tracker = BudgetTracker()
    tracker.db = MagicMock()  # Mock the database to isolate tests
    return tracker

def test_login_success(tracker):
    tracker.db.get_user.return_value = (1, "test_user")
    tracker.login()
    assert tracker.current_user is not None
    assert tracker.current_user[1] == "test_user"

def test_login_failure(tracker):
    tracker.db.get_user.return_value = None
    tracker.login()
    assert tracker.current_user is None
