import pytest
from app import create_app
from config import Config


class TestConfig(Config):
    TESTING = True


@pytest.fixture(scope="session")
def app():
    """Create and configure a new app instance for each test session."""
    app = create_app(TestConfig)

    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture(scope="function")
def client(app):
    """A test client for the app."""
    return app.test_client()
