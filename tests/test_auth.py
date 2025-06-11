def test_register_success(client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/auth/register' endpoint is posted to (POST) with a new username and password
    THEN check that the response is 201 and a success message is returned
    """
    response = client.post(
        "/api/auth/register",
        json={"username": "testuser_success", "password": "password123"},
    )
    data = response.get_json()

    assert response.status_code == 201
    assert data["message"] == "User created successfully."


def test_register_duplicate_user(client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/auth/register' endpoint is posted to (POST) with a username that already exists
    THEN check that the response is 400 and an error message is returned
    """
    # First, register the user to create the duplicate condition
    user_data = {"username": "testuser_duplicate", "password": "password123"}
    client.post("/api/auth/register", json=user_data)

    # Then, attempt to register the same user again
    response = client.post("/api/auth/register", json=user_data)
    data = response.get_json()

    assert response.status_code == 400
    assert data["message"] == "Username already exists."


def test_register_missing_password(client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/auth/register' endpoint is posted to (POST) without a password
    THEN check that the response is 400 and a validation error is returned
    """
    response = client.post(
        "/api/auth/register",
        json={"username": "testuser_missing_pass"},
    )
    data = response.get_json()

    assert response.status_code == 400
    assert data["message"] == "Password is required."


def test_register_missing_username(client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/auth/register' endpoint is posted to (POST) without a username
    THEN check that the response is 400 and a validation error is returned
    """
    response = client.post(
        "/api/auth/register",
        json={"password": "some_password"},
    )
    data = response.get_json()

    assert response.status_code == 400
    assert data["message"] == "Username is required."


def test_login_success(client, init_database):
    """
    GIVEN a Flask application configured for testing and a registered user
    WHEN the '/api/auth/login' endpoint is posted to (POST) with correct credentials
    THEN check that the response is 200 and an access token is returned
    """
    # First, register a user to log in with
    user_data = {"username": "testuser_login", "password": "password123"}
    register_response = client.post("/api/auth/register", json=user_data)
    assert register_response.status_code == 201

    # Attempt to log in
    login_response = client.post("/api/auth/login", json=user_data)
    data = login_response.get_json()

    assert login_response.status_code == 200
    assert "access_token" in data


def test_login_invalid_credentials(client, init_database):
    """
    GIVEN a Flask application configured for testing and a registered user
    WHEN the '/api/auth/login' endpoint is posted to (POST) with an incorrect password
    THEN check that the response is 401 and an error message is returned
    """
    # Register a user
    user_data = {"username": "testuser_badpass", "password": "password123"}
    register_response = client.post("/api/auth/register", json=user_data)
    assert register_response.status_code == 201

    # Attempt to log in with the wrong password
    response = client.post(
        "/api/auth/login",
        json={"username": "testuser_badpass", "password": "wrongpassword"},
    )
    data = response.get_json()

    assert response.status_code == 401
    assert data["message"] == "Bad username or password."


def test_login_nonexistent_user(client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/auth/login' endpoint is posted to (POST) with a username that does not exist
    THEN check that the response is 401 and an error message is returned
    """
    response = client.post(
        "/api/auth/login",
        json={"username": "nonexistentuser", "password": "somepassword"},
    )
    data = response.get_json()

    assert response.status_code == 401
    assert data["message"] == "Bad username or password."