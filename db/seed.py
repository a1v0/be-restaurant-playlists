import psycopg2

playlists = [{"name": "playlist_1", "tags": ["leeds", "chinese"], "owner": "jjjjj"}, {"name": "playlist_2", "tags": ["manchester", "american"], "owner": "jjjjj"}]

connection = psycopg2.connect(
    # host = "", database = "", user = "", password = ""
    )

connection.autocommit = True

def create_playlists (cursor) -> None:
    cursor.execute(""" DROP TABLE """)