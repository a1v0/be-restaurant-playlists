import pytest
from db.seed import seed
from db.seed_data.test_data import playlists, users, restaurants, votes
from db.connection import connection, pool, cursor
from app import app
import json
from ast import literal_eval

# PYTHONPATH=$(pwd) py.test <optional keyword searches with -k -v>

# utility functions

def create_dict(byte):
    return literal_eval(byte.decode('utf-8'))

# tests

@pytest.fixture
def test_app():
    test_app = app
    test_app.config.update(
        {
            "TESTING": True,
        }
    )
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
    vote_count_values = []
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
        vote_count_values.append(playlist["vote_count"])
    assert vote_count_values == ['5.0', '4.0', '1.0'], "test failed"
    for i in range(len(vote_count_values)):
        vote_number = float(vote_count_values[i])
        if vote_count_values[i] > 
            print("its greater than or equal to")
        
    
# for loop to get each value in the array
# compare each value with the next value
# may need to coerce into a number
    

@pytest.mark.request_specific_playlist  # this is showing as a warning
def test_request_specific_playlist_success(client):
    response = client.get("/api/playlists/1")
    playlistBytes = response.data
    playlist = json.loads(playlistBytes.decode("utf-8"))

    assert response.status == "200 OK", "incorrect http response"
    assert type(playlist["playlist"]) == list, "Test failed"

    for playlist in playlist["playlist"]:
        assert playlist["playlist_id"] == 1, "Test failed"
        assert "name" in playlist, "Test failed"
        assert "place_id" in playlist, "Test failed"
        assert "location" in playlist, "Test failed"
        assert "cuisine" in playlist, "Test failed"
        assert "owner_nickname" in playlist, "Test failed"
        assert "description" in playlist, "Test failed"


def test_request_specific_playlist_valid_but_nonexistent_playlist_id(client):
    response = client.get("/api/playlists/1000000")
    playlistBytes = response.data
    playlist = json.loads(playlistBytes.decode("utf-8"))

    assert response.status == "404 NOT FOUND", "incorrect http response"
    assert playlist["msg"] == "playlist not found"


def test_request_specific_playlist_invalid_playlist_id(client):
    response = client.get("/api/playlists/sdfghjkl")
    playlistBytes = response.data
    playlist = json.loads(playlistBytes.decode("utf-8"))

    assert response.status == "400 BAD REQUEST", "incorrect http response"
    assert playlist["msg"] == "invalid playlist id"
