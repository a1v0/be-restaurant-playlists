from psycopg2.pool import SimpleConnectionPool
from os import environ
from dotenv import dotenv_values
import psycopg2.extras


env = ".env.development"

# sets environment variable in case of testing
if "PYTEST_CURRENT_TEST" in environ:
    env = ".env.test"
    # *** TO DO *** needs provision for production environment

config = {**dotenv_values(env)}  # returns the contents of specified .env file
environ["PG_DATABASE"] = config["PG_DATABASE"]

pool = SimpleConnectionPool(minconn=1, maxconn=10, database=environ["PG_DATABASE"])
connection = pool.getconn()
cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
pool.putconn(connection)

connection.autocommit = True  # no idea what this does but it's super important
