import json

from healthcheck_api import db, create_app
from healthcheck_api.entries import EntryModel
import unittest


class TestEntry(unittest.TestCase):

    def setUp(self):
        self.app = create_app({'TESTING': True})
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            new_entry = EntryModel('test_entry')
            db.session.add(new_entry)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_entries(self):
        response = self.client.get('/entries')
        assert response.json == [{"id": 1, "name": 'test_entry'}]

    def test_create_entry(self):
        response = self.client.post('/entries',
                                    data=json.dumps({"name": "test_entry"}),
                                    content_type='application/json')
        assert response.json == {"id": 2, "name": 'test_entry'}

    def test_get_entry(self):
        response = self.client.get('/entries/1')
        assert response.json == {"id": 1, "name": 'test_entry'}

    def test_update_entry(self):
        response = self.client.put('/entries/1',
                                   data=json.dumps({"name": "new_name"}),
                                   content_type='application/json')
        assert response.json == {"id": 1, "name": 'new_name'}

    def test_delete_entry(self):
        response = self.client.delete('/entries/1')
        assert response.status_code == 204
