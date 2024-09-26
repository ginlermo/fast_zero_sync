from http import HTTPStatus

from tests.conftest import TodoFactory


def test_create_todo(client, token):
    response = client.post(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Todo",
            "description": "Test todo description",
            "state": "draft",
        },
    )

    assert response.json() == {
        "id": 1,
        "title": "Test Todo",
        "description": "Test todo description",
        "state": "draft",
    }


def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_pagination_should_return_2_todos(
    session, user, client, token
):
    expected_todos = 2
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        "/todos/?offset=1&limit=2",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_return_correct_title_todos_and_return_5(
    session, client, user, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, title="Test Todo 1")
    )
    session.commit()

    response = client.get(
        "/todos/?title=Test Todo 1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_return_correct_description_todos_and_return_5(
    session, client, user, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, description="description")
    )
    session.commit()

    response = client.get(
        "/todos/?description=desc",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_return_correct_state_todos_and_return_5(
    session, client, user, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, state="done")
    )
    session.commit()

    response = client.get(
        "/todos/?state=done",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_list_todos_return_combined_todos_and_return_5(
    session, client, user, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            title="Test Todo 1",
            description="Test todo description 1",
            state="done",
        )
    )

    session.bulk_save_objects(
        TodoFactory.create_batch(
            2,
            user_id=user.id,
            title="Test Todo 2",
            description="Test todo description 2",
            state="draft",
        )
    )

    session.commit()

    response = client.get(
        "/todos/?title=Test Todo 1&description=Test todo description "
        "1&state=done",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["todos"]) == expected_todos


def test_delete_todo(client, user, token, session):
    session.bulk_save_objects(TodoFactory.create_batch(1, user_id=user.id))
    session.commit()
    response = client.delete(
        "/todos/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "message": "Todo has been deleted successfully."
    }


def test_delete_todo_error(client, user, token, session):
    response = client.delete(
        "/todos/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Todo not found."}


def test_patch_todo(client, user, token, session):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.patch(
        f"/todos/{todo.id}",
        json={"title": "testing_patch"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == "testing_patch"


def test_patch_todo_error(client, user, token, session):
    response = client.patch(
        "/todos/2",
        json={"title": "testing_patch"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Todo not found."}
