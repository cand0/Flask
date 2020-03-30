from flask import Flask, render_template
import sqlite3

from cand0.challenges import challenges
from cand0.auth import auth
from cand0.teams import teams
from cand0.scoreboard import scoreboard
from cand0.admin import admin

app = Flask(__name__)

app.secret_key = 'session_secret_key'

@app.route("/")
@app.route("/index/")
def index():
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	cur.execute("select NAME, MESSAGE from HINT")
	hints = cur.fetchall()

	conn.close()
	return render_template('index.html', hints = hints)
@app.route("/test/")
@app.route("/test.html/")
def test():
	return render_template('test.html')

app.register_blueprint(challenges)
app.register_blueprint(auth)
app.register_blueprint(teams)
app.register_blueprint(scoreboard)
app.register_blueprint(admin)
