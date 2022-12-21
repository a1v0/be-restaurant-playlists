import pytest
from db.seed import seed
from db.seed_data.test_data import playlists, users, restaurants, votes
from db.connection import connection, pool, cursor
from app import app
import psycopg2.extras


# PYTHONPATH=$(pwd) py.test <optional keyword searches with -k -v>

@pytest.fixture
def test_app():
    test_app = app
    test_app.config.update({
        "TESTING": True,
    })
    # other setup can go here
    try: 
        seed(playlists, users, restaurants, votes)
    except: 
        try:
            cursor.close()
        except: 
            connection.close()
            connection = pool.getconn()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    yield test_app

    # clean up / reset resources here
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



