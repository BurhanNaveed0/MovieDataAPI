import json
import scraper
import sqlite3
import threading
import time
from flask import Flask, request


app = Flask(__name__)
con = sqlite3.connect("movie_data.db", check_same_thread=False)
con.row_factory = sqlite3.Row


@app.route('/', methods=['GET'])
def query_db_records():
    cur = con.cursor()
    cur.execute("SELECT * FROM movie_data")

    return [dict(row) for row in cur.fetchall()]


def db_update():
    print("DATA UPDATED")

    cur = con.cursor()
    movie_data = scraper.scrape_lifetime_gross()
    cur.execute("DELETE FROM movie_data")
    con.commit()

    for row in movie_data:
        cur.execute("INSERT INTO movie_data VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                    row)
    con.commit()


def handle_background_task():
    while True:
        db_update()
        time.sleep(60)


def db_setup():
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS movie_data(rank, name, year, worldLifetimeGross, domesticLifetimeGross
    , foreignLifetimeGross, domesticPercentage, foreignPercentage)""")


if __name__ == "__main__":
    db_setup()
    cached_update_thread = threading.Thread(target=handle_background_task)
    cached_update_thread.start()
    app.run(debug=True)
