import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry
from fast_zero.security import get_password_hash


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    """
    Creates a session with an in-memory SQLite database.

    Returns:
        Session: The created session object.

    Raises:
        None
    """
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    # live 43/151 - explicação sobre with e yield
    # with - gerenciamento de contexto
    # yield - retorna o valor e continua a execução
    with Session(engine) as session:
        yield session  # arrange

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    pwd = 'test_pass'

    user = User(
        username='test_user_name',
        email='teste@teste.com',
        password=get_password_hash(pwd),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # Monkey patching

    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
