import pytest
import mongomock

from app import create_app


@pytest.fixture()
def app():
    mongo_client = mongomock.MongoClient()
    application = create_app({
        "TESTING": True,
        "SECRET_KEY": "test",
        "MONGO_DB_NAME": "opstrack_test",
        "MONGO_CLIENT_FACTORY": lambda *_args, **_kwargs: mongo_client,
    })
    yield application


@pytest.fixture()
def client(app):
    return app.test_client()
