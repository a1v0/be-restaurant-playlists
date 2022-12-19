import psycopg2

playlists = [
    {
        "name": "playlist_1",
        "description": "lorem ipsum lorem ipsum",
        "location": "leeds",
        "cuisine": "chinese",
        "owner_email": "ymca@restaurant-playlists.com",
    },
    {
        "name": "playlist_2",
        "description": "lorem ipsum lorem ipsum",
        "location": "manchester",
        "cuisine": "american",
        "owner_email": "ymca2@restaurant-playlists.com",
    },
]

users = [
    {
        "user_email": "ymca@restaurant-playlists.com",
        "nickname": "ymca",
        "avatar_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/800px-Image_created_with_a_mobile_phone.png",
    },
    {
        "user_email": "ymca2@restaurant-playlists.com",
        "nickname": "ymca2",
        "avatar_url": "https://images.ctfassets.net/hrltx12pl8hq/3j5RylRv1ZdswxcBaMi0y7/b84fa97296bd2350db6ea194c0dce7db/Music_Icon.jpg",
    },
]

restaurants = [
    {"playlist_id": 1, "place_id": "ChIJ3-SMG6FeeUgRGKtBhlH0fhY"},
    {"playlist_id": 1, "place_id": "ChIJwf5pV8bme0gRWrquuGBndA8"},
    {"playlist_id": 1, "place_id": "ChIJbQIhL6FeeUgRd4YGS3CdRgk"},
    {"playlist_id": 2, "place_id": "ChIJP8J3ZIVeeUgRlzmWlDEjXPc"},
    {"playlist_id": 2, "place_id": "ChIJK9qnyBlceUgR0ahqyr73-qs"},
    {"playlist_id": 2, "place_id": "ChIJmWR08-5deUgRIPZKe0zjFEg"},
]

votes = [{"playlist_id": 1, "vote_count": 4}, {"playlist_id": 2, "vote_count": 1}]

connection = psycopg2.connect(
    # *** TO DO *** Make database dynamic depending on environment
    database="restaurant_playlists_test"
    # host = "", user = "", password = ""
)

connection.autocommit = True


def create_users_table(cursor) -> None:
    cursor.execute(
        """ 
    DROP TABLE IF EXISTS users CASCADE;
    CREATE TABLE users 
    (
        user_email VARCHAR(200) PRIMARY KEY,
        nickname VARCHAR(200) NOT NULL,
        avatar_url VARCHAR NOT NULL
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
        """,
            (user["user_email"], user["nickname"], user["avatar_url"]),
        )


def create_playlists_table(cursor) -> None:
    cursor.execute(
        """ 
    DROP TABLE IF EXISTS playlists CASCADE;
    CREATE TABLE playlists 
    (
        playlist_id SERIAL PRIMARY KEY, 
        name VARCHAR(100) NOT NULL,
        description TEXT,
        location VARCHAR(50),
        cuisine VARCHAR(50),
        owner_email VARCHAR REFERENCES users(user_email) ON DELETE CASCADE NOT NULL
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
        """,
            (
                playlist["name"],
                playlist["description"],
                playlist["location"],
                playlist["cuisine"],
                playlist["owner_email"],
            ),
        )


def create_restaurants_table(cursor) -> None:
    cursor.execute(
        """ 
    DROP TABLE IF EXISTS restaurants;
    CREATE TABLE restaurants 
    (
       restaurant_id SERIAL PRIMARY KEY,
       playlist_id INT REFERENCES playlists(playlist_id) ON DELETE CASCADE NOT NULL,
       place_id VARCHAR NOT NULL
    )
    """
    )


with connection.cursor() as cursor:
    create_restaurants_table(cursor)
    for restaurant in restaurants:
        cursor.execute(
            """
        INSERT INTO restaurants
            (
            playlist_id, place_id
            ) 
        VALUES (
        %s, %s
        )
        """,
            (restaurant["playlist_id"], restaurant["place_id"]),
        )


def create_votes_table(cursor) -> None:
    cursor.execute(
        """ 
    DROP TABLE IF EXISTS votes;
    CREATE TABLE votes 
    (
      vote_id SERIAL PRIMARY KEY,
      playlist_id INT REFERENCES playlists(playlist_id) ON DELETE CASCADE NOT NULL,
      vote_count INT NOT NULL CHECK (vote_count BETWEEN 0 AND 5) NOT NULL
    )
    """
    )


with connection.cursor() as cursor:
    create_votes_table(cursor)
    for vote in votes:
        cursor.execute(
            """
        INSERT INTO votes
            (
            playlist_id, vote_count
            ) 
        VALUES (
        %s, %s
        )
        """,
            (vote["playlist_id"], vote["vote_count"]),
        )
