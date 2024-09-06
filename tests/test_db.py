from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username="ginlermo",
        email="ginlermo@email.com",
        password="blablabla",
    )

    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == "ginlermo@email.com")
    )

    assert result.id == 1
    assert result.username == "ginlermo"
    assert result.email == "ginlermo@email.com"
    assert result.password == "blablabla"
