import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def session():
    """
    Creates a session with an in-memory SQLite database.

    Returns:
        Session: The created session object.

    Raises:
        None
    """
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    # live 43/151 - explicação sobre with e yield
    # with - gerenciamento de contexto
    # yield - retorna o valor e continua a execução
    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
