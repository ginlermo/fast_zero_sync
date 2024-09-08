from jwt import decode

from fast_zero.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data_jwt = {"sub": "test_user"}

    token = create_access_token(data_jwt)

    result = decode(token, SECRET_KEY, algorithms=ALGORITHM)

    assert result["sub"] == data_jwt["sub"]
    assert result["exp"]
