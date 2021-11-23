import json

from healthcheck_api import db, create_app
from healthcheck_api.entries import EntryModel
import unittest


class TestEntryModule(unittest.TestCase):

    def setUp(self):
        self.app = create_app({'TESTING': True})
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_entries(self):
        with self.app.app_context():
            new_entry = EntryModel('test_entry')
            db.session.add(new_entry)
            db.session.commit()

        response = self.client.get('/entries')
        assert response.json == [{"id": 1, "name": 'test_entry'}]

    def test_create_entry(self):
        response = self.client.post('/entries',
                                    data=json.dumps({"name": "test_entry"}),
                                    content_type='application/json')
        assert response.json == {"id": 1, "name": 'test_entry'}

    def test_get_entry(self):
        with self.app.app_context():
            new_entry = EntryModel('test_entry')
            db.session.add(new_entry)
            db.session.commit()

        response = self.client.get('/entries/1')
        assert response.json == {"id": 1, "name": 'test_entry'}
