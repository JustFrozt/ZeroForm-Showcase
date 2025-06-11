def test_create_note_success(client, auth_headers_user_one):
    """
    GIVEN a valid user and authentication token
    WHEN a POST request is made to /api/notes with valid data
    THEN check for a 201 status code and correct note data in response
    """
    note_data = {"title": "My First Note", "content": "This is the content."}

    res = client.post("/api/notes", headers=auth_headers_user_one, json=note_data)
    response_data = res.get_json()

    assert res.status_code == 201
    assert response_data["title"] == note_data["title"]
    assert response_data["content"] == note_data["content"]
    assert "id" in response_data
    assert "user_id" in response_data


def test_create_note_unauthorized(client):
    """
    GIVEN a request to create a note
    WHEN the request is made without an Authorization header
    THEN check for a 401 Unauthorized status code
    """
    note_data = {"title": "Unauthorized Note", "content": "This should fail."}
    res = client.post("/api/notes", json=note_data)
    assert res.status_code == 401


def test_get_all_notes_success(client, auth_headers_user_one):
    """
    GIVEN a user with multiple notes
    WHEN a GET request is made to /api/notes
    THEN check for a 200 status code and a list of the user's notes
    """
    # Create a couple of notes for the user
    client.post(
        "/api/notes",
        headers=auth_headers_user_one,
        json={"title": "Note 1", "content": "Content 1"},
    )
    client.post(
        "/api/notes",
        headers=auth_headers_user_one,
        json={"title": "Note 2", "content": "Content 2"},
    )

    res = client.get("/api/notes", headers=auth_headers_user_one)
    response_data = res.get_json()

    assert res.status_code == 200
    assert isinstance(response_data, list)
    assert len(response_data) == 2
    assert response_data[0]["title"] == "Note 1"
    assert response_data[1]["title"] == "Note 2"


def test_get_single_note_success(client, auth_headers_user_one, created_note):
    """
    GIVEN a user has created a note
    WHEN a GET request is made to /api/notes/<note_id> for that note
    THEN check for a 200 status code and the correct note data
    """
    note_id = created_note["id"]

    res = client.get(f"/api/notes/{note_id}", headers=auth_headers_user_one)
    response_data = res.get_json()

    assert res.status_code == 200
    assert response_data["id"] == note_id
    assert response_data["title"] == created_note["title"]


def test_get_note_not_found(client, auth_headers_user_one):
    """
    GIVEN a valid user and authentication token
    WHEN a GET request is made for a non-existent note ID
    THEN check for a 404 Not Found status code
    """
    res = client.get("/api/notes/99999", headers=auth_headers_user_one)
    assert res.status_code == 404


def test_get_note_from_another_user(client, created_note, auth_headers_user_two):
    """
    GIVEN two users, where User A has a note
    WHEN User B tries to GET User A's note
    THEN check for a 404 Not Found status code (for security)
    """
    note_id = created_note["id"]  # This note belongs to user one
    res = client.get(f"/api/notes/{note_id}", headers=auth_headers_user_two)
    assert res.status_code == 404


def test_update_note_success(client, auth_headers_user_one, created_note):
    """
    GIVEN a user has created a note
    WHEN a PUT request is made to /api/notes/<note_id> with new data
    THEN check for a 200 status code and that the note data is updated
    """
    note_id = created_note["id"]

    update_data = {"title": "Updated Title", "content": "Updated Content"}
    res = client.put(
        f"/api/notes/{note_id}",
        headers=auth_headers_user_one,
        json=update_data,
    )
    response_data = res.get_json()

    assert res.status_code == 200
    assert response_data["title"] == update_data["title"]
    assert response_data["content"] == update_data["content"]


def test_update_note_from_another_user(client, created_note, auth_headers_user_two):
    """
    GIVEN two users, where User A has a note
    WHEN User B tries to PUT an update to User A's note
    THEN check for a 404 Not Found status code
    """
    note_id = created_note["id"]
    res = client.put(
        f"/api/notes/{note_id}",
        headers=auth_headers_user_two,
        json={"title": "Malicious Update"},
    )

    assert res.status_code == 404


def test_delete_note_success(client, auth_headers_user_one, created_note):
    """
    GIVEN a user has created a note
    WHEN a DELETE request is made to /api/notes/<note_id>
    THEN check for a 200 status code and that the note is subsequently gone
    """
    note_id = created_note["id"]

    delete_res = client.delete(f"/api/notes/{note_id}", headers=auth_headers_user_one)
    assert delete_res.status_code == 200
    assert delete_res.get_json()["message"] == "Note deleted."

    # Verify the note is gone
    get_res = client.get(f"/api/notes/{note_id}", headers=auth_headers_user_one)
    assert get_res.status_code == 404


def test_delete_note_from_another_user(client, created_note, auth_headers_user_two):
    """
    GIVEN two users, where User A has a note
    WHEN User B tries to DELETE User A's note
    THEN check for a 404 Not Found status code
    """
    note_id = created_note["id"]
    res = client.delete(f"/api/notes/{note_id}", headers=auth_headers_user_two)
    assert res.status_code == 404