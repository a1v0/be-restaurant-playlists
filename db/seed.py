from test_data import playlists, users, restaurants, votes
from connection import connection


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
