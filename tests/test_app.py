from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello World"}


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "test_user",
            "password": "test_pwd",
            "email": "test@test.com",
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        "username": "test_user",
        "id": 1,
        "email": "test@test.com",
    }


def test_read_user_without_user(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_user(client, user):
    user_public = UserPublic.model_validate(user)
    user_schema = user_public.model_dump()
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_update_user(client, user):
    response = client.put(
        "/users/1",
        json={
            "username": "test_user",
            "email": "test@test.com",
            "password": "test_pwd",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "test_user",
        "email": "test@test.com",
        "id": 1,
    }


def test_delete_user(client, user):
    response = client.delete("/users/1")
    assert response.json() == {"message": "User deleted"}


def test_username_already_registered(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "test_user",
            "password": "test_pwd",
            "email": "test@test.com",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 2,
        "username": "test_user",
        "email": "test@test.com",
    }

    response = client.post(
        "/users/",
        json={
            "username": "test_user",
            "password": "new_test_pwd",
            "email": "new_test@test.com",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username already exists"}


def test_email_already_registered(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "test_user",
            "password": "test_pwd",
            "email": "test@test.com",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 2,
        "username": "test_user",
        "email": "test@test.com",
    }

    response = client.post(
        "/users/",
        json={
            "username": "test_user_for_email",
            "password": "test_pwd",
            "email": "test@test.com",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Email already exists"}


def test_not_found_id_for_edit_user(client):
    response = client.put(
        "/users/2",
        json={
            "username": "test_user",
            "email": "test@test.com",
            "password": "test_pwd",
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_not_found_id_for_delete_user(client):
    response = client.delete(
        "/users/2",
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_existent_get_user(client, user):
    existent_user = client.get("/users/1/")
    assert existent_user.status_code == HTTPStatus.OK


def test_not_existent_get_user(client):
    response = client.get("/users/999/")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}
