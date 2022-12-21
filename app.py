from flask import Flask, jsonify, request
from db.connection import connection, cursor
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route("/api/playlists", methods=["GET"])
def all_playlists():
    if request.method == "GET":
        cursor.execute("SELECT * FROM playlists;")
        playlists = cursor.fetchall()
        results = json.dumps({"playlists":playlists})
        loaded_results = json.loads(results)
        cursor.close()
        connection.close()
        return loaded_results



