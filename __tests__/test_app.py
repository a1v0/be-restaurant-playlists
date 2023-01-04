from os import environ
import pytest


environ[
    "PYTEST_CURRENT_TEST"
] = ""  # This ensures that the connection file selects the correct environment
from db.seed import seed
from db.seed_data.test_data import playlists, users, restaurants, votes
from app import app
import json

# PYTHONPATH=$(pwd) py.test -rP
# <optional keyword searches with -k -v>


# utility functions


def create_dict(byte):
    return json.loads(byte.decode("utf-8"))


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
    count = 0
    assert response.status == "200 OK", "Test Failed"
    for playlist in array:
        assert "cuisine" in playlist, "test failed"
        assert "description" in playlist, "test failed"
        assert "location" in playlist, "test failed"
        assert "name" in playlist, "test failed"
        assert "owner_email" not in playlist, "test failed"
        assert "playlist_id" in playlist, "test failed"
        assert "vote_count" in playlist, "test failed"
        assert "total_votes" in playlist, "test failed"
        assert "nickname" in playlist, "test failed"
        vote_count_values.append(playlist["vote_count"])
    for i in range(len(vote_count_values)):
        if count != len(vote_count_values) - 1:
            vote_number1 = float(vote_count_values[i])
            vote_number2 = float(vote_count_values[i + 1])
            assert vote_number1 >= vote_number2, "test_failed"
            count = count + 1


@pytest.mark.ticket_6
def test_get_200_playlist_by_location(client):
    response = client.get("/api/playlists?location=leeds")
    result = create_dict(response.data)
    array = result["playlists"]
    for playlist in array:
        assert playlist["location"] == "leeds", "test failed"


@pytest.mark.ticket_6
def test_get_404_playlist_non_existent_location(client):
    response = client.get("/api/playlists?location=sdfghjkl")
    result = create_dict(response.data)

    assert response.status == "404 NOT FOUND", "incorrect http response"
    assert result["msg"] == "invalid location / cuisine tag", "incorrect msg"


@pytest.mark.ticket_6
def test_get_200_playlist_by_cuisine(client):
    response = client.get("/api/playlists?cuisine=thai")
    result = create_dict(response.data)
    array = result["playlists"]
    assert len(array) > 0, "test failed"
    for playlist in array:
        assert playlist["cuisine"] == "thai", "test failed"


@pytest.mark.ticket_6
def test_get_404_playlist_by_non_existent_cuisine(client):
    response = client.get("/api/playlists?cuisine=aaaaaa")
    result = create_dict(response.data)

    assert response.status == "404 NOT FOUND", "incorrect http response"
    assert result["msg"] == "invalid location / cuisine tag", "incorrect msg"


@pytest.mark.ticket_6
def test_get_200_playlist_by_both(client):
    response = client.get("/api/playlists?location=leeds&cuisine=thai")
    result = create_dict(response.data)
    array = result["playlists"]
    assert len(array) > 0, "test failed"
    for playlist in array:
        assert playlist["location"] == "leeds", "test failed"
        assert playlist["cuisine"] == "thai", "test failed"


@pytest.mark.ticket_6
def test_get_404_playlist_non_existent_location_and_cuisine(client):
    response = client.get("/api/playlists?location=zzzzz&cuisine=aaaaaa")
    result = create_dict(response.data)

    assert response.status == "404 NOT FOUND", "incorrect http response"
    assert result["msg"] == "invalid location / cuisine tag", "incorrect msg"


@pytest.mark.ticket_6
def test_get_404_playlist_by_valid_location_and_non_existent_cuisine(client):
    response = client.get("/api/playlists?location=leeds&cuisine=aaaaaa")
    result = create_dict(response.data)

    assert response.status == "404 NOT FOUND", "incorrect http response"
    assert result["msg"] == "invalid location / cuisine tag", "incorrect msg"


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


@pytest.mark.post_new_user  # this is showing as a warning
def test_post_new_user(client):
    response = client.post(
        "/api/users",
        json={
            "user_email": "someone@example.com",
            "nickname": "Myself",
            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwlrNQyIFCa1XnXF1Ex8lSuOHhHaWxd3_zWR2m3j6Tig&s",
        },
    )
    user_bytes = response.data
    user = json.loads(user_bytes.decode("utf-8"))
    assert response.status == "201 CREATED", "incorrect http response"
    assert user["user"]["user_email"] == "someone@example.com"
    assert user["user"]["nickname"] == "Myself"
    assert (
        user["user"]["avatar_url"]
        == "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwlrNQyIFCa1XnXF1Ex8lSuOHhHaWxd3_zWR2m3j6Tig&s"
    )


def test_post_new_user_with_excess_data(client):
    response = client.post(
        "/api/users",
        json={
            "useless_property": "useless_value",
            "user_email": "someone@example.com",
            "nickname": "Myself",
            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwlrNQyIFCa1XnXF1Ex8lSuOHhHaWxd3_zWR2m3j6Tig&s",
        },
    )
    user_bytes = response.data
    user = json.loads(user_bytes.decode("utf-8"))
    assert response.status == "201 CREATED", "incorrect http response"
    assert user["user"]["user_email"] == "someone@example.com"
    assert user["user"]["nickname"] == "Myself"
    assert (
        user["user"]["avatar_url"]
        == "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwlrNQyIFCa1XnXF1Ex8lSuOHhHaWxd3_zWR2m3j6Tig&s"
    )
    assert user["user"].get("useless_property") is None


def test_post_new_user_with_incomplete_data(client):
    response = client.post(
        "/api/users",
        json={
            "nickname": "Myself",
        },
    )
    user_bytes = response.data
    user = json.loads(user_bytes.decode("utf-8"))
    assert response.status == "400 BAD REQUEST", "incorrect http response"
    assert user["msg"] == "Invalid Request Body"


def test_post_new_user_with_existing_email(client):
    response = client.post(
        "/api/users",
        json={
            "user_email": "ymca@restaurant-playlists.com",
            "nickname": "Myself",
            "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSwlrNQyIFCa1XnXF1Ex8lSuOHhHaWxd3_zWR2m3j6Tig&s",
        },
    )
    user_bytes = response.data
    user = json.loads(user_bytes.decode("utf-8"))
    assert response.status == "400 BAD REQUEST", "incorrect http response"
    assert user["msg"] == "UniqueViolation: email already registered"


@pytest.mark.post_new_playlist  # this is showing as a warning
def test_post_new_playlist(client):
    response = client.post(
        "/api/playlists",
        json={
            "name": "Yousif's playlist",
            "description": "My playlist nice description",
            "location": "Nice Location",
            "cuisine": "Seafood",
            "owner_email": "ymca2@restaurant-playlists.com",
        },
    )
    assert response.status == "201 CREATED", "incorrect http response"
    playlist_bytes = response.data
    playlist_json = json.loads(playlist_bytes.decode("utf-8"))
    playlist = playlist_json["playlist"]
    assert type(playlist) == dict
    assert playlist["name"] == "Yousif's playlist"
    assert playlist["description"] == "My playlist nice description"
    assert playlist["location"] == "Nice Location"
    assert playlist["cuisine"] == "Seafood"
    assert playlist["owner_email"] == "ymca2@restaurant-playlists.com"


def test_post_new_playlist_with_extra_info(client):
    response = client.post(
        "/api/playlists",
        json={
            "name": "Yousif's playlist",
            "description": "My playlist nice description",
            "location": "Nice Location",
            "cuisine": "Seafood",
            "owner_email": "ymca2@restaurant-playlists.com",
            "useless_property": "useless info",
        },
    )
    assert response.status == "201 CREATED", "incorrect http response"
    playlist_bytes = response.data
    playlist_json = json.loads(playlist_bytes.decode("utf-8"))
    playlist = playlist_json["playlist"]
    assert "useless_property" not in playlist


def test_post_new_playlist_with_missing_mandatory_data(client):
    response = client.post(
        "/api/playlists",
        json={
            "name": "Yousif's playlist",
            "description": "My playlist nice description",
            "location": "Nice Location",
            "cuisine": "Seafood",
        },
    )
    assert response.status == "400 BAD REQUEST", "incorrect http response"
    msg_bytes = response.data
    msg_json = json.loads(msg_bytes.decode("utf-8"))
    assert msg_json["msg"] == "Invalid Request Body"


def test_post_new_playlist_owner_not_in_db(client):
    response = client.post(
        "/api/playlists",
        json={
            "name": "Yousif's playlist",
            "description": "My playlist nice description",
            "location": "Nice Location",
            "cuisine": "Seafood",
            "owner_email": "boo@restaurant-playlists.com",
        },
    )
    assert response.status == "400 BAD REQUEST", "incorrect http response"
    msg_bytes = response.data
    msg_json = json.loads(msg_bytes.decode("utf-8"))
    assert msg_json["msg"] == "Email address not registered"


@pytest.mark.patch_existing_playlist  # this is showing as a warning
def test_patch_playlist(client):
    response = client.patch(
        "/api/playlists/1",
        json={
            "name": "Yousif",
            "description": "Any desc",
            "location": "somewhere",
            "cuisine": "food",
        },
    )
    playlist_bytes = response.data
    playlist_json = json.loads(playlist_bytes.decode("utf-8"))
    playlist = playlist_json["playlist"]
    assert response.status == "200 OK", "incorrect http response"
    assert type(playlist) == dict
    assert playlist["name"] == "Yousif"
    assert playlist["description"] == "Any desc"
    assert playlist["location"] == "somewhere"
    assert playlist["cuisine"] == "food"
    assert playlist["playlist_id"] == 1


def test_patch_playlist_with_only_one_data_field(client):
    response = client.patch(
        "/api/playlists/1",
        json={
            "cuisine": "any kind of food",
        },
    )
    playlist_bytes = response.data
    playlist_json = json.loads(playlist_bytes.decode("utf-8"))
    playlist = playlist_json["playlist"]
    assert response.status == "200 OK", "incorrect http response"
    assert playlist["playlist_id"] == 1
    assert playlist["cuisine"] == "any kind of food"


def test_patch_playlist_ignores_irrelevant_fields(client):
    response = client.patch(
        "/api/playlists/1",
        json={"cuisine": "any kind of food", "hello": "goodbye"},
    )
    playlist_bytes = response.data
    playlist_json = json.loads(playlist_bytes.decode("utf-8"))
    playlist = playlist_json["playlist"]
    assert response.status == "200 OK", "incorrect http response"
    assert playlist["playlist_id"] == 1
    assert playlist["cuisine"] == "any kind of food"


def test_patch_playlist_with_nonexistent_but_valid_playlist_id(client):
    response = client.patch(
        "/api/playlists/100000",
        json={
            "cuisine": "any kind of food",
        },
    )
    playlist_bytes = response.data
    playlist_json = json.loads(playlist_bytes.decode("utf-8"))
    msg = playlist_json["msg"]
    assert response.status == "404 NOT FOUND", "incorrect http response"
    assert msg == "playlist not found"


def test_patch_playlist_with_invalid_playlist_id(client):
    response = client.patch(
        "/api/playlists/asdfjsdfkjsfh",
        json={
            "cuisine": "any kind of food",
        },
    )
    playlist_bytes = response.data
    playlist_json = json.loads(playlist_bytes.decode("utf-8"))
    msg = playlist_json["msg"]
    assert response.status == "400 BAD REQUEST", "incorrect http response"
    assert msg == "invalid playlist id"


# Delete tests


@pytest.mark.delete_existing_playlist  # this is showing as a warning
def test_delete_playlist_with_id(client):
    response = client.delete("/api/playlists/1")
    assert response.status == "204 NO CONTENT", "incorrect http response"


@pytest.mark.delete_existing_playlist  # this is showing as a warning
def test_delete_playlist_non_existing_id(client):
    response = client.delete("/api/playlists/5000")
    assert response.status == "404 NOT FOUND", "incorrect http response"
    msg_bytes = response.data
    msg_json = json.loads(msg_bytes.decode("utf-8"))
    msg = msg_json["msg"]
    assert msg == "playlist not found"


@pytest.mark.delete_existing_playlist  # this is showing as a warning
def test_delete_playlist_invalid_id(client):
    response = client.delete("/api/playlists/oeirjg32")
    assert response.status == "400 BAD REQUEST", "incorrect http response"
    msg_bytes = response.data
    msg_json = json.loads(msg_bytes.decode("utf-8"))
    msg = msg_json["msg"]
    assert msg == "invalid playlist id"


@pytest.mark.playlists_by_user  # this is showing as a warning
def test_get_playlists_by_user(client):
    response = client.get("/api/users/ymca@restaurant-playlists.com/playlists")
    assert response.status == "200 OK", "incorrect http response"
    result = create_dict(response.data)
    array = result["playlists"]
    vote_count_values = []
    count = 0
    for playlist in array:
        assert "cuisine" in playlist, "test failed"
        assert "description" in playlist, "test failed"
        assert "location" in playlist, "test failed"
        assert "name" in playlist, "test failed"
        assert "owner_email" not in playlist, "test failed"
        assert "playlist_id" in playlist, "test failed"
        assert "vote_count" in playlist, "test failed"
        assert "total_votes" in playlist, "test failed"
        assert "nickname" in playlist, "test failed"
        vote_count_values.append(playlist["vote_count"])
    for i in range(len(vote_count_values)):
        if count != len(vote_count_values) - 1:
            vote_number1 = float(vote_count_values[i])
            vote_number2 = float(vote_count_values[i + 1])
            assert vote_number1 >= vote_number2, "test_failed"
            count = count + 1


# we'll never get a 404 from this test, unless we add a potentially unnecessary extra db request. The DB query finds no results for an invalid email but doesn't think this is a problem.
# in theory, we'll only (for now) be making a request to see the logged-in user's playlists. Since you can't be logged in if your email isn't in the DB, this shouldn't cause an issue

# @pytest.mark.playlists_by_user  # this is showing as a warning
# def test_get_playlists_by_nonexistent_user(client):
#     response = client.get("/api/users/23456789098765434567890987654rtyu/playlists")
#     assert response.status == "404 NOT FOUND", "incorrect http response"
#     result = create_dict(response.data)
#     msg = result["msg"]
#     assert msg == "user not found"

@pytest.mark.ticket_14_post_new_vote
def test_post_new_votes_happy_path(client):
    response = client.post(
        "/api/votes",
        json={
            "playlist_id": 1,
            "vote_count": 2,
        },
    )
    assert response.status == "201 CREATED", "incorrect http response"
    votes_bytes = response.data
    votes_json = json.loads(votes_bytes.decode("utf-8"))
    votes = votes_json["votes"]
    assert type(votes) == list
    assert votes[0]["playlist_id"] == 1
    assert votes[0]["vote_count"] == 2

@pytest.mark.ticket_14_post_new_vote
def test_post_new_votes_invalid_playlist_id(client):
    response = client.post(
        "/api/votes",
        json={
            "playlist_id": 1000,
            "vote_count": 2,
        },
    )
    assert response.status == "400 BAD REQUEST", "incorrect http response"
    msg_bytes = response.data
    msg_json = json.loads(msg_bytes.decode("utf-8"))
    msg = msg_json["msg"]


@pytest.mark.restaurants_by_playlist_id
def test_post_restaurants_happy_path(client):
    response = client.post(
        "/api/playlists/1/restaurants", json={
            "place_ids": ["ChIJP8J3ZIVeeUgRlzmWlDEjXPc", "ChIJmWR08-5deUgRIPZKe0zjFEg"]
        }
    )
    assert response.status == "201 CREATED", "incorrect http response"
    restaurants_bytes = response.data
    restaurants_json = json.loads(restaurants_bytes.decode("utf-8"))
    restaurants = restaurants_json["restaurants"]
    assert type(restaurants) == list
    assert len(restaurants) == 2
    assert restaurants[0]["place_id"] ==  "ChIJP8J3ZIVeeUgRlzmWlDEjXPc"

@pytest.mark.restaurants_by_playlist_id
def test_post_restaurants_invalid_playlist(client):
    response = client.post(
        "/api/playlists/1000/restaurants", json={
            "place_ids": ["ChIJP8J3ZIVeeUgRlzmWlDEjXPc", "ChIJmWR08-5deUgRIPZKe0zjFEg"]
        }
    )
    assert response.status == "400 BAD REQUEST", "incorrect http response"
    restaurants_bytes = response.data
    restaurants_json = json.loads(restaurants_bytes.decode("utf-8"))
    msg = restaurants_json["msg"]

    assert msg == "playlist does not exist"