import os
import pytest

from healthcheck_api import create_app, db
from healthcheck_api.entries import EntryModel


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
    yield app

    os.environ['DATABASE_URL'] = conn_string


@pytest.fixture()
def db_client():
    app = create_app({'TESTING': True})
    client = app.test_client()
    with app.app_context():
        db.create_all()
        new_entry = EntryModel('test_entry')
        db.session.add(new_entry)
        db.session.commit()
        yield client
        db.session.remove()
        db.drop_all()
