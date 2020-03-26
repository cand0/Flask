from flask import Flask, render_template, Blueprint
import sqlite3

scoreboard = Blueprint('scoreboard', __name__)

@scoreboard.route('/scoreboard/')
def scoreboardmain():
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	cur.execute("select NAME, SCORE from team order by SCORE desc, AUTH_TIME desc")
	score = cur.fetchall()
	len_score = len(score)

	conn.close()

	return render_template("scoreboard.html", len_score = len_score,score = score)
