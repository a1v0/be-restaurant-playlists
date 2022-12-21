import pytest
from db.seed import seed
from db.seed_data.test_data import playlists, users, restaurants, votes
from db.connection import connection, pool
from app import all_playlists

seed()

# PYTHONPATH=$(pwd) py.test <optional keyword searches with -k -v>

# @pytest.fixture
# def setup():
#     # before each
#     seed(playlists, users, restaurants, votes)

# @pytest.mark.usefixtures("setup")
def test_response():
    # input = all_playlists()
    assert 1 == 1, "Test Failed"


