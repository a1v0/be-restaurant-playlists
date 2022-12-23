from flask import Flask, jsonify, request
from db.connection import connection, cursor
from flask_cors import CORS
import json
import psycopg2.errors

app = Flask(__name__)
CORS(app)


@app.route("/api/playlists", methods=["GET", "POST"])
def all_playlists():
    if request.method == "GET":
        cursor.execute(
            """
        SELECT playlists.playlist_id, playlists.name, playlists.description, playlists.location, playlists.cuisine, users.nickname, CAST(CAST(AVG(votes.vote_count) AS DECIMAL(10, 1)) AS VARCHAR(4)) AS vote_count FROM playlists
        LEFT JOIN votes
        ON playlists.playlist_id = votes.playlist_id 
        LEFT JOIN users
        ON playlists.owner_email = users.user_email
        GROUP BY playlists.playlist_id, users.nickname
        ORDER BY vote_count DESC;
        """
        )
        playlists = cursor.fetchall()
        results = json.dumps({"playlists": playlists})
        loaded_results = json.loads(results)
        return loaded_results

    if request.method == "POST":
        # Eventhough some fields are not mandatory, the front-end must always send all fields.
        post_body = request.get_json()
        if "owner_email" not in post_body or "name" not in post_body:
            return return_invalid_request_body()
        try:
            cursor.execute(
                """
            INSERT INTO playlists (name, description, location, cuisine, owner_email)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *;
            """,
                (
                    post_body["name"],
                    post_body["description"],
                    post_body["location"],
                    post_body["cuisine"],
                    post_body["owner_email"],
                ),
            )
            new_playlist = cursor.fetchall()
            results = json.dumps({"playlist": new_playlist[0]})
            loaded_results = json.loads(results)
            return loaded_results, 201

        except psycopg2.errors.ForeignKeyViolation:
            return jsonify({"msg": "Email address not registered"}), 400


@app.route("/api/playlists/<playlist_id>", methods=["GET", "PATCH"])
def specific_playlist(playlist_id):
    try:
        int(playlist_id)
    except:
        return jsonify({"msg": "invalid playlist id"}), 400
    if request.method == "GET":
        cursor.execute(
            """
                SELECT
                    name,
                    place_id,
                    nickname AS owner_nickname,
                    location,
                    cuisine,
                    description,
                    playlists.playlist_id
                FROM playlists
                INNER JOIN restaurants
                ON playlists.playlist_id = restaurants.playlist_id
                INNER JOIN users
                ON owner_email = user_email
                WHERE playlists.playlist_id = %s;
            """,
            [playlist_id],
        )
        playlist = cursor.fetchall()
        results = json.dumps({"playlist": playlist})
        loaded_results = json.loads(results)
        # *** TO DO *** ensure that it's not possible to submit an empty playlist to the site, so that there will always be content to be displayed, so long as the playlist_id is valid
        if len(loaded_results["playlist"]) == 0:
            return jsonify({"msg": "playlist not found"}), 404
        else:
            return loaded_results
    if request.method == "PATCH":
        patch_body = request.get_json()
        query_string = """UPDATE playlists
        SET """
        valid_fields = ["name", "description", "location", "cuisine"]

        injected_fields = []
        for i in range(len(valid_fields)):
            if valid_fields[i] in patch_body:
                query_string += f"{valid_fields[i]} = %s"
                injected_fields.append(patch_body[valid_fields[i]])
                if i != len(valid_fields) - 1:
                    query_string += ", "

        query_string += """
                WHERE playlist_id = %s
                RETURNING *;
            """
        injected_fields.append(playlist_id)
        cursor.execute(
            query_string,
            injected_fields,
        )
        playlist = cursor.fetchall()
        try:
            results = json.dumps({"playlist": playlist[0]})
        except IndexError:
            return jsonify({"msg": "playlist not found"}), 404
        loaded_results = json.loads(results)
        return loaded_results


@app.route("/api/users", methods=["POST"])
def users():
    post_body = request.get_json()
    if (
        post_body.get("user_email") is None
        or post_body.get("nickname") is None
        or post_body.get("avatar_url") is None
    ):
        return return_invalid_request_body()

    if request.method == "POST":
        try:
            cursor.execute(
                """
            INSERT INTO users (user_email, nickname, avatar_url)
            VALUES
            (%s,%s,%s)
            RETURNING *;
            """,
                (
                    post_body["user_email"],
                    post_body["nickname"],
                    post_body["avatar_url"],
                ),
            )
            new_user = cursor.fetchall()
            results = json.dumps({"user": new_user[0]})
            loaded_results = json.loads(results)
            return loaded_results, 201
        except psycopg2.errors.UniqueViolation:
            return jsonify({"msg": "UniqueViolation: email already registered"}), 400


# Utility functions
def return_invalid_request_body():
    return jsonify({"msg": "Invalid Request Body"}), 400
