import pytest
from database import Database

@pytest.fixture
def db():
    # Setup: Create an instance of the Database class
    database = Database()
    yield database
    # Teardown: Close the database connection after tests
    database.close()

def test_add_user(db):
    username = "test_user"
    assert db.add_user(username) == True  # Check if user is added successfully
    assert db.get_user(username) is not None  # Check if user can be retrieved

def test_add_user_duplicate(db):
    username = "test_user"
    db.add_user(username)
    assert db.add_user(username) == False  # Adding duplicate should fail
