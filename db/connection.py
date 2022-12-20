import psycopg2
from os import environ

if "PYTEST_CURRENT_TEST" in environ:
    # *** TO DO *** Check whether pytest actually adds this to the environment variables, or whether we need to add it manually
    environ["PG_DATABASE"] = "restaurant_playlists_test"
else:
    environ["PG_DATABASE"] = "restaurant_playlists"
    # *** TO DO *** needs provision for production environment


connection = psycopg2.connect(
    database=environ["PG_DATABASE"]
    # host = "", user = "", password = ""
)

connection.autocommit = True
