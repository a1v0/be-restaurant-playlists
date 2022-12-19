import psycopg2
from os import environ

environ["PG_DATABASE"] = "restaurant_playlists_test"

connection = psycopg2.connect(
    # *** TO DO *** Make database dynamic depending on environment
    database=environ["PG_DATABASE"]
    # host = "", user = "", password = ""
)

connection.autocommit = True
