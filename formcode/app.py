# https://www.tutorialspoint.com/flask/flask_sqlite.htm
# http://flask.pocoo.org/docs/0.12/patterns/sqlite3/
# https://github.com/stevedunford/NZVintageRadios

import sqlite3
from flask import Flask, Response, render_template, abort

# Creates a Flask object called 'app' that we can use throughout the programme
app = Flask(__name__)

# This is the function that controls the main page of the web site
@app.route("/")
def index():
  return render_template('main.html',
                          title="Check the Track")

# This is the function shows the Athletes page
@app.route("/athletes")
def athletes():

  conn = sqlite3.connect('db/tracks.db')
  cursor = conn.cursor()
  results = cursor.execute("SELECT TrackName,Difficulty,Conditions,Date from Tracks")
  medalists = [dict(track=row[0], difficulty=row[1], conditions=row[2], date=row[3]) for row in results]
  return render_template('athletes.html', title="Tracks", medalists=medalists)

@app.route("/login")
def login():
  
  return render_template('login.html', title="Login")  

# This function deals with any missing pages and shows the Error page
@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html', title="404"), 404

if __name__ == "__main__":
    app.run(debug=True)



