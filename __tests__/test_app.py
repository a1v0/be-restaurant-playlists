import pytest
from db.seed import seed
from db.seed_data.test_data import playlists, users, restaurants, votes
from db.connection import connection, pool, cursor
from app import app
from ast import literal_eval

# PYTHONPATH=$(pwd) py.test <optional keyword searches with -k -v>

@pytest.fixture
def test_app():
    test_app = app
    test_app.config.update({
        "TESTING": True,
    })
    seed(playlists, users, restaurants, votes)
    yield test_app

@pytest.fixture()
def client(test_app):
    return test_app.test_client()

@pytest.fixture()
def runner(test_app):
    return test_app.test_cli_runner()

@pytest.mark.ticket_5
def test_get_playlists_keys(client):
    response = client.get("/api/playlists")
    result = create_dict(response.data)
    array = result["playlists"]
    print(array)
    assert response.status == "200 OK", "Test Failed"
    for playlist in array:
        assert 'cuisine' in playlist, "test failed"
        assert 'description' in playlist, "test failed"
        assert 'location' in playlist, "test failed"
        assert 'name' in playlist, "test failed"
        assert 'owner_email' in playlist, "test failed"
        assert 'playlist_id' in playlist, "test failed"
        assert 'vote_count' in playlist, "test failed"
        assert 'nickname' in playlist, "test failed"
    

# utility functions

def create_dict(byte):
    return literal_eval(byte.decode('utf-8'))
