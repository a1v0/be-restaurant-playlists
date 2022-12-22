from flask import Flask, jsonify, request
from db.connection import connection, cursor
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route("/api/playlists", methods=["GET"])
def all_playlists():
    if request.method == "GET":
        cursor.execute("""
        SELECT playlists.*, users.nickname, CAST(CAST(AVG(votes.vote_count) AS DECIMAL(10, 1)) AS VARCHAR(4)) AS vote_count FROM playlists
        LEFT JOIN votes
        ON playlists.playlist_id = votes.playlist_id 
        LEFT JOIN users
        ON playlists.owner_email = users.user_email
        GROUP BY playlists.playlist_id, users.nickname;
        """)
        playlists = cursor.fetchall()
        results = json.dumps({"playlists":playlists})
        loaded_results = json.loads(results)
        return loaded_results



