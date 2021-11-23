import json


def test_root(client, benchmark):
    benchmark(client.get, '/')


def test_healthcheck(client, benchmark):
    benchmark(client.get, '/healthcheck')


def test_db_error(db_error_client, benchmark):
    benchmark(db_error_client.get, '/')


def test_get_entries(db_client, benchmark):
    benchmark(db_client.get, '/entries')


def test_create_entry(db_client, benchmark):
    benchmark(db_client.post, '/entries', data=json.dumps({"name": "test_entry"}), content_type='application/json')


def test_get_entry(db_client, benchmark):
    benchmark(db_client.get, '/entries/1')


def test_update_entry(db_client, benchmark):
    benchmark(db_client.put, '/entries/1', data=json.dumps({"name": "new_name"}), content_type='application/json')


def test_delete_entry(db_client, benchmark):
    benchmark(db_client.delete, '/entries/1')
