import psycopg2

playlists = [{"name": "playlist_1", "description": "lorem ipsum lorem ipsum", "location": "leeds", "cuisine": "chinese", "owner_email": "ymca@restaurant-playlists.com"}, {"name": "playlist_2", "description": "lorem ipsum lorem ipsum", "location": "manchester", "cuisine": "american", "owner_email": "ymca2@restaurant-playlists.com"}]

users = [{"user_email": "ymca@restaurant-playlists.com", "nickname": "ymca", "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/800px-Image_created_with_a_mobile_phone.png"},{"user_email": "ymca2@restaurant-playlists.com", "nickname": "ymca2", "avatar_url": "https://images.ctfassets.net/hrltx12pl8hq/3j5RylRv1ZdswxcBaMi0y7/b84fa97296bd2350db6ea194c0dce7db/Music_Icon.jpg"}]

connection = psycopg2.connect(
    # *** TO DO *** Make database dynamic depending on environment
    database = "restaurant_playlists_test"
    # host = "", user = "", password = ""
    )

connection.autocommit = True

def create_users_table (cursor) -> None:
    cursor.execute(
    """ 
    DROP TABLE IF EXISTS users CASCADE;
    CREATE TABLE users 
    (
        user_email VARCHAR(200) PRIMARY KEY,
        nickname VARCHAR(200),
        avatar_url VARCHAR
    )
    """
    ) 

with connection.cursor() as cursor:
    create_users_table(cursor)
    for user in users:
        cursor.execute(
        """
        INSERT INTO users
            (
            user_email, nickname, avatar_url
            ) 
        VALUES (
        %s, %s, %s
        )
        """, (user["user_email"], user["nickname"], user["avatar_url"])
         )

def create_playlists_table (cursor) -> None:
    cursor.execute(
    # ***TO DO*** For owner column make a reference to the user table
    """ 
    DROP TABLE IF EXISTS playlists;
    CREATE TABLE playlists 
    (
        playlist_id SERIAL PRIMARY KEY, 
        name VARCHAR(100),
        description TEXT,
        location VARCHAR(50),
        cuisine VARCHAR(50),
        owner_email VARCHAR REFERENCES users(user_email) ON DELETE CASCADE
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
            name, description, location, cuisine, owner_email
            ) 
        VALUES (
        %s, %s, %s, %s, %s
        )
        """, (playlist["name"], playlist["description"], playlist["location"], playlist["cuisine"], playlist["owner_email"])
         )

