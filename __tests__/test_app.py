import pytest
from db.seed import seed
from db.seed_data.test_data import playlists, users, restaurants, votes
from db.connection import connection, pool, cursor
from app import app
import json

# PYTHONPATH=$(pwd) py.test <optional keyword searches with -k -v>


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


def test_request_example(client):
    response = client.get("/api/playlists")
    assert response.status == "200 OK", "Test Failed"


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
