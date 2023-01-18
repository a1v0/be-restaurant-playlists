from psycopg2.pool import SimpleConnectionPool
from os import environ
from dotenv import dotenv_values
import psycopg2.extras
import urllib.parse as up

# environ["ENVIRONMENT"] = ".env.production"
env = environ["ENVIRONMENT"] if "ENVIRONMENT" in environ else ".env.development"

# sets environment variable in case of testing
if "PYTEST_CURRENT_TEST" in environ:
    env = ".env.test"

config = {**dotenv_values(env)}  # returns the contents of specified .env file
host = ""
environ["PG_DATABASE"] = config["PG_DATABASE"]
database = environ["PG_DATABASE"]
user = ""
password = ""
host = ""
port = ""

if "ENVIRONMENT" in environ:
    environ["DATABASE_URL"] = config["DATABASE_URL"]
    up.uses_netloc.append("postgres")
    url = up.urlparse(environ["DATABASE_URL"])
    database = url.path[1:]
    host = url.hostname
    user = url.username
    password = url.password
    port = url.port


pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    database=database,
    host=host,
    user=user,
    password=password,
    port=port,
)
connection = pool.getconn()
cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
pool.putconn(connection)

connection.autocommit = True  # no idea what this does but it's super important
