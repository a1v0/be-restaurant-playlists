from flask import Flask, jsonify
from db.connection import connection

app = Flask(__name__)


@app.route("/api", methods=["GET"])
def all_playlists():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM playlists;")
    playlists = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(playlists)


# this is only necessary for Cyrus, if he can't fix his PC
# if __name__ == "__main__":
#     print(__name__)
#     app.run(debug=True, port=8001)
