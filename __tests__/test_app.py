# import os
# import pytest
# import sys
# sys.path.append("../db")

# from db.seed import seed
# from db.seed_data.test_data import playlists, users, restaurants, votes
# from db.connection import connection, pool
# from app import all_playlists

# seed()

# @pytest.fixture
# def setup():
#     # before each
#     seed(playlists, users, restaurants, votes)

# @pytest.mark.usefixtures("setup")
# def test_response(setup):
#     input = all_playlists()
#     assert 1 == 1, "Test Failed"

import os
import sys

current = os.path.dirname(os.path.realpath(__file__))

parent = os.path.dirname(current)

sys.path.append(parent)

import db.seed
import db.connection

db.seed.seed()
