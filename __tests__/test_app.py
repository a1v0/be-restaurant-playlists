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
    print(response.data)
    assert response.status == "200 OK", "Test Failed"


@pytest.mark.request_specific_playlist  # this is showing as a warning
def test_request_specific_playlist(client):
    response = client.get("/api/playlists/1")
    playlistBytes = response.data
    playlist = json.loads(playlistBytes.decode("utf-8"))
    print(playlist)
    assert type(playlist["playlist"]) == list
    for playlist in playlist["playlist"]:
        assert playlist["playlist_id"] == 1
        assert "name" in playlist
        assert "place_id" in playlist
        assert "location" in playlist
        assert "cuisine" in playlist
        assert "owner_nickname" in playlist
        assert "description" in playlist
