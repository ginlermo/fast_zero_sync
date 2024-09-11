from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_access_token, settings


def test_jwt():
    data_jwt = {"sub": "test_user"}

    token = create_access_token(data_jwt)

    result = decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

    assert result["sub"] == data_jwt["sub"]
    assert result["exp"]


def test_jwt_invalid_token(client):
    response = client.delete(
        "/users/1", headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
