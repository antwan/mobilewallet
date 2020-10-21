import pytest
from alembic import command
from alembic.config import Config
from starlette.config import environ
from starlette.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

import nest_asyncio
nest_asyncio.apply()

environ["TESTING"] = "True"
environ["SECRET"] = "TESTING"


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """
    Create a clean database on every test case.
    For safety, we should abort if a database already exists.

    We use the `sqlalchemy_utils` package here for a few helpers in consistently
    creating and dropping the database.
    """
    from src import settings

    url = str(settings.TEST_DATABASE_URL)
    engine = create_engine(url)
    assert not database_exists(url), "Test database already exists. Aborting tests."
    create_database(url)  # Create the test database.
    config = Config("migrations/alembic.ini")  # Run the migrations.
    command.upgrade(config, "head")
    yield  # Run the tests.
    drop_database(url)  # Drop the test database.


@pytest.fixture()
def client():
    """
    When using the 'client' fixture in test cases, we'll get full database
    rollbacks between test cases:

    def test_homepage(client):
        url = app.url_path_for('homepage')
        response = client.get(url)
        assert response.status_code == 200
    """
    from src.app import app

    with TestClient(app) as client:
        yield client
