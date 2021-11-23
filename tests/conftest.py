import os
import pytest

from healthcheck_api import create_app


@pytest.fixture
def app():
    app = create_app({'TESTING': True})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_error_client():
    conn_string = os.environ['DATABASE_URL']

    os.environ['DATABASE_URL'] = 'invalid_conn_string'
    app = create_app({'TESTING': True}).test_client()

    os.environ['DATABASE_URL'] = conn_string
    return app

