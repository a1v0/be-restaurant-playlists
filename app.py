import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="restaurant_playlists_test")
    return conn

@app.route('/')

def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM playlists;')
    playlists = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', playlists=playlists)

if __name__ == '__main__':
    print(__name__)
    app.run(debug=True, port=8001)






















