from http import HTTPStatus


def test_read_root_must_return_ok_and_hello_world(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello World"}


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "ginlermo",
            "password": "password",
            "email": "ginlermo@email.com",
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        "username": "ginlermo",
        "id": 1,
        "email": "ginlermo@email.com",
    }


def test_get_specific_user(client):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        "username": "ginlermo",
        "id": 1,
        "email": "ginlermo@email.com",
    }


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "mynewpassword",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_delete_user(client):
    response = client.delete("/users/1")
    assert response.json() == {"message": "User deleted"}
