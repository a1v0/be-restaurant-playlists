from flask import Flask, jsonify, request
from db.connection import connection, cursor
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


@app.route("/api/playlists", methods=["GET"])
def all_playlists():
    if request.method == "GET":
        location = request.args.get("location")
        cuisine = request.args.get("cuisine")
        sql_condition = []
        starting_query = """
                SELECT playlists.playlist_id, playlists.name, playlists.description, playlists.location, playlists.cuisine, users.nickname, CAST(CAST(AVG(votes.vote_count) AS DECIMAL(10, 1)) AS VARCHAR(4)) AS vote_count FROM playlists
                LEFT JOIN votes
                ON playlists.playlist_id = votes.playlist_id 
                LEFT JOIN users
                ON playlists.owner_email = users.user_email
                """  
        if location: 
            appended_query = starting_query + """ WHERE playlists.location = %s """
            sql_condition.append(location)

        if cuisine:
            appended_query = starting_query + """ WHERE playlists.cuisine = %s """
            sql_condition.append(cuisine)

        final_query = appended_query + """GROUP BY playlists.playlist_id, users.nickname
                ORDER BY vote_count DESC;"""

        cursor.execute(final_query, sql_condition)
        playlists = cursor.fetchall()
        results = json.dumps({"playlists": playlists})
        loaded_results = json.loads(results)
        return loaded_results, 200


@app.route("/api/playlists/<playlist_id>", methods=["GET"])
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


@app.route("/api/users", methods=["POST"])
def users():
    post_body = request.get_json()
    if (
        post_body.get("user_email") is None
        or post_body.get("nickname") is None
        or post_body.get("avatar_url") is None
    ):
        return jsonify({"msg": "Invalid Request Body"}),400

    if request.method == "POST":
        cursor.execute(
            """
        INSERT INTO users (user_email, nickname, avatar_url)
        VALUES
        (%s,%s,%s)
        RETURNING *;
        """,
            (post_body["user_email"], post_body["nickname"], post_body["avatar_url"]),
        )
    new_user = cursor.fetchall()
    results = json.dumps({"user": new_user[0]})
    loaded_results = json.loads(results)
    return loaded_results, 201
