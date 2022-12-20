import psycopg2
from os import environ

if "PYTEST_CURRENT_TEST" in environ:
    environ["PG_DATABASE"] = "restaurant_playlists_test"
else:
    environ["PG_DATABASE"] = "restaurant_playlists"
    # needs provision for production environment

connection = psycopg2.connect(
    database=environ["PG_DATABASE"]
    # host = "", user = "", password = ""
)

connection.autocommit = True
