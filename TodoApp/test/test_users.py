import pytest
from fastapi import status
from .utils import override_get_current_user, override_get_db, client, TestingSessionLocal, engine
from ..main import app
from ..routers.Users import get_current_user, get_db
from ..routers.auth import bcrypt_context
from sqlalchemy import text
from ..models import Users


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture
def test_user():
    user = Users(
        username = 'abhivardhantest',
        email = 'abhivardhan@gmail.com',
        first_name='abhi',
        last_name='reddy',
        hashed_password = bcrypt_context.hash('abhivardhan'),
        role = "admin",
        phone_number = "7601051016"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users "))
        connection.commit()

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'abhivardhantest'
    assert response.json()['first_name'] == 'abhi'
    assert response.json()['last_name'] == 'reddy'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '7601051016'
    assert response.json()['email'] == 'abhivardhan@gmail.com'


def test_change_password_success(test_user):
    response = client.put("/user/password", json={"password": "abhivardhan",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/password", json={"password": "abhvardhan",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()=={'detail':'Error on password change'}


def test_change_phone_number_success(test_user):
    response = client.post("/user/phonenumber/7601051015")
    assert response.status_code == status.HTTP_204_NO_CONTENT


