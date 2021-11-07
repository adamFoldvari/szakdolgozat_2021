from healthcheck_api import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_root(client):
    response = client.get('/')
    assert response.json == { "success": True }


def test_healthcheck(client):
    response = client.get('/healthcheck')
    assert response.json == { "success": True }
