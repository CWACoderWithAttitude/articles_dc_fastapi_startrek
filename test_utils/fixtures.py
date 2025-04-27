from typing import Any, Generator
from sqlmodel.pool import StaticPool

from fastapi.testclient import TestClient
from main import app
from routers.ships_router import get_session
import pytest
from sqlmodel import SQLModel, Session, create_engine


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, Any, None]:
    """
    Create a test client for the FastAPI app.
    This way we can depedency inject the test client into every test case."""

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    # clear the dependency overrides after the test
    app.dependency_overrides.clear()
