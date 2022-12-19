import psycopg2

playlists = [{"name": "playlist_1", "location": "leeds", "cuisine": "chinese", "owner_email": "ymca@restaurant-playlists.com"}, {"name": "playlist_2", "location": "manchester", "cuisine": "american", "owner_email": "ymca@restaurant-playlists.com"}]

connection = psycopg2.connect(
    # *** TO DO *** Make database dynamic depending on environment
    database = "restaurant_playlists_test"
    # host = "", user = "", password = ""
    )

connection.autocommit = True

def create_playlists_table (cursor) -> None:
    cursor.execute(
    # ***TO DO*** For owner column make a reference to the user table
    """ 
    DROP TABLE IF EXISTS playlists;
    CREATE TABLE playlists 
    (
        playlist_id SERIAL PRIMARY KEY, 
        name VARCHAR(100),
        location VARCHAR(50),
        cuisine VARCHAR(50),
        owner_email VARCHAR(100)
    )
    """
    ) 

with connection.cursor() as cursor:
    create_playlists_table(cursor)
    for playlist in playlists:
        cursor.execute(
        """
        INSERT INTO playlists
            (
            name, location, cuisine, owner_email
            ) 
        VALUES (
        %s, %s, %s, %s
        )
        """, (playlist["name"], playlist["location"], playlist["cuisine"], playlist["owner_email"])
         )

#  {playlist["name"]},
#         {playlist["location"]},
#         {playlist["cuisine"]},
#         {playlist["owner_email"]}

        #  cursor.execute(
        # """
        #  INSERT INTO playlists VALUES
        #     (
        #     %(name)s,
        #     %(location)s,
        #     %(cuisine)s,
        #     %(owner_email)s,
        #     );
        # """, **playlist
        #  )