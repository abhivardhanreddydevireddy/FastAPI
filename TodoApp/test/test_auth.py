



from ..main import app
from ..routers.auth import get_db, authenticate_user,create_access_token,SECRET_KEY,ALGORITHM,get_current_user
from .utils import override_get_db, TestingSessionLocal, engine
from ..routers.auth import bcrypt_context
from ..models import Users
from sqlalchemy import text
from jose import jwt
from datetime import  timedelta
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def test_user():
    user = Users(
        username='abhivardhantest',
        email='abhivardhan@gmail.com',
        first_name='abhi',
        last_name='reddy',
        hashed_password=bcrypt_context.hash('abhivardhan'),
        role="admin",
        phone_number="7601051016"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()

def test_authenticate_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, 'abhivardhan', db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user('WrongUserName', 'testpassword',db)
    assert non_existent_user is False

    wrong_password_user = authenticate_user(test_user.username, 'wrongpassword', db)
    assert wrong_password_user is False


def test_create_access_token():
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)
    token = create_access_token(username, user_id, role, expires_delta)  # ← add this
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],
                               options={"verify_signature": False})

    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub':'testuser','id':1,'role':'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token=token)
    assert user == {'username': 'testuser', 'id': 1, 'role': 'admin'}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role':'user'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Could not validate credentials'