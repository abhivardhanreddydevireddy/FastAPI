import pytest
from TodoApp.models import Todos
from sqlalchemy import text
from starlette import status
from .utils import override_get_db, override_get_current_user, client, app, TestingSessionLocal, engine
from ..routers.admin import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture
def test_todo():
    todo = Todos(
        title="learn to code",
        description="need to learn everyday",
        priority=5,
        completed=False,
        owner_id=1,
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM todos;'))
        connection.commit()

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'completed': False, 'title': 'learn to code',
                                'description': 'need to learn everyday', 'id': 1,
                                'priority': 5, 'owner_id': 1}]


def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_admin_delete_todo_not_found(test_todo):
    response = client.delete("/admin/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail':'Todo not found'}