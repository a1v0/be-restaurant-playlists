import psycopg2
from os import environ


if environ["PYTEST_CURRENT_TEST"]:
    environ["PG_DATABASE"] = "restaurant_playlists_test"
else:
    # this database doesn't exist yet...
    environ["PG_DATABASE"] = "restaurant_playlists"
    # needs provision for production environment

connection = psycopg2.connect(
    database=environ["PG_DATABASE"]
    # host = "", user = "", password = ""
)

connection.autocommit = True
