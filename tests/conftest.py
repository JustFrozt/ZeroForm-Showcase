import pytest
from app import create_app
from app.config import TestingConfig
from app.extensions import db


@pytest.fixture(scope="module")
def app():
    """Module-level fixture to create a Flask app instance for testing."""
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="module")
def client(app):
    """Module-level fixture to provide a test client for the app."""
    return app.test_client()


@pytest.fixture(scope="function")
def init_database(app):
    """Function-level fixture to ensure a clean database for each test."""
    with app.app_context():
        # A fast way to clear all data from all tables
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
    yield db


@pytest.fixture(scope="function")
def registered_user_one(client, init_database):
    """Registers a user and returns their credentials."""
    user_data = {"username": "testuser1", "password": "password123"}
    client.post("/api/auth/register", json=user_data)
    return user_data


@pytest.fixture(scope="function")
def auth_headers_user_one(client, registered_user_one):
    """Logs in the registered user and returns authentication headers."""
    res = client.post("/api/auth/login", json=registered_user_one)
    access_token = res.get_json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture(scope="function")
def registered_user_two(client, init_database):
    """Registers a second, different user."""
    user_data = {"username": "testuser2", "password": "456"}
    client.post("/api/auth/register", json=user_data)
    return user_data


@pytest.fixture(scope="function")
def auth_headers_user_two(client, registered_user_two):
    """Logs in the second user and returns their authentication headers."""
    res = client.post("/api/auth/login", json=registered_user_two)
    access_token = res.get_json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture(scope="function")
def created_note(client, auth_headers_user_one):
    """Creates a note for user one and returns the created note data from the API response."""
    note_data = {"title": "Test Note 1", "content": "This is content for the first note."}
    response = client.post("/api/notes", json=note_data, headers=auth_headers_user_one)
    return response.get_json()
