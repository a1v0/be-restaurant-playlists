import pytest
from db.run_seed import seed
from db.seed_data.test_data import playlists, users, restaurants, votes
from db.connection import connection, pool

@pytest.fixture
def setup():
    # before each
    seed(playlists, users, restaurants, votes)

    # after each
