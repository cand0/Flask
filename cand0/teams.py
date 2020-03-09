from flask import Flask, render_template, url_for, request, redirect, session, escape, Blueprint
import sqlite3

teams = Blueprint('teams', __name__)

@teams.route("/teams/")
@teams.route("/teams/<name>")
def team(name = None):
	option = 0;

	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	#find team list
	cur.execute("select NAME, LEADER, SCORE from TEAM")
	teams = cur.fetchall()

	#Go to our team
	if 'ID' in session:
		cur.execute("select TEAM_NAME from USER where ID='%s'"%session['ID'])
		my_team = cur.fetchall()

	if name != None:
		cur.execute("select ID ,MESSAGE from USER where TEAM_NAME='%s'"%name)
		users = cur.fetchall()

		#select team information
		cur.execute("select NAME, LEADER, SCORE from TEAM where NAME='%s'"%name)
		sel_team = cur.fetchall()

		#Modify My Team
		for chk_user in users:
			if chk_user[0] == session['ID'] :
				option = 1;
				break;

		return render_template("team.html",teams=teams , name = name, users = users, sel_team = sel_team[0], my_team = my_team[0][0], option = option)
	elif 'ID' in session:
		return redirect(url_for('teams.team', name = session['ID']))
	else :
		return render_template("team.html", teams=teams, option = option)

@teams.route("/team-proc/", methods=['POST'])
def teamproc():
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	#update user
	MESSAGE = request.form['MESSAGE']
	cur.execute("UPDATE USER SET MESSAGE = ? WHERE ID = ?", (MESSAGE, session['ID']))

	#find my team
	cur.execute("select TEAM_NAME from USER where ID = '%s'"%session['ID'])
	my_team = cur.fetchall()

	conn.commit()
	conn.close()

	return redirect(url_for('teams.team', name = my_team[0][0]))
