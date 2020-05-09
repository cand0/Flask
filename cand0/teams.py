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
	cur.execute("select NAME from TEAM where HIDDEN = '0'")
	teams = cur.fetchall()
	#Go to my team
	my_team = []
	if 'ID' in session:
		cur.execute("select TEAM_NAME from USER where ID='%s'"%session['ID'])
		my_team = cur.fetchall()
	#parameter check
	if name != None:
		cur.execute("select ID ,MESSAGE from USER where TEAM_NAME='%s'"%name)
		users = cur.fetchall()

		#select team information
		cur.execute("select NAME, LEADER, SCORE from TEAM where NAME='%s'"%name)
		sel_team = cur.fetchall()
		#team solves
		cur.execute("select CHALLENGE_NAME from SOLVES where USER_TEAM_NAME = '%s'"%name)
		team_solves = cur.fetchall()

		#Modify My Team
		option = 0	#option0 : other, option1 : me
		for chk_user in users:
			if 'ID' in session:
				if chk_user[0] == session['ID'] :
					option = 1
					break
		if name == 'WAIT_TEAM':
			return render_template("team.html", teams=teams, my_team = my_team, option = option)
		return render_template("team.html",teams=teams, name = name, users = users, sel_team = sel_team, my_team = my_team, option = option, team_solves = team_solves)

	if 'ID' in session:
		return redirect(url_for('teams.team', name = my_team[0][0]))
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

@teams.route("/team-manage/")
def teammanage():
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	#find team list
	cur.execute("select NAME from TEAM")
	teams = cur.fetchall()
	#Go to my team
	cur.execute("select TEAM_NAME from USER where ID='%s'"%session['ID'])
	my_team = cur.fetchall()
	#team manage
	cur.execute("select ID, MESSAGE from user where ID in (select USER_ID from TEAM_WAIT where TEAM_ID = '%s')"%my_team[0][0])
	team_users = cur.fetchall()

	conn.close()
	return render_template("team-manage.html", teams=teams, my_team = my_team, team_users = team_users)

@teams.route("/team-manage-proc/<name>")
def teammanageproc(name = None):
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	#user team
	cur.execute("select TEAM_ID from TEAM_WAIT where USER_ID = '%s'"%name)
	user_team = cur.fetchall()

	#leader OK?
	cur.execute("select LEADER from TEAM where NAME = '%s'"%user_team[0][0])
	team_leader = cur.fetchall()

	if team_leader[0][0] == session['ID']:
		sql = "update user set TEAM_NAME = '%s' where ID = '%s'"%(user_team[0][0], name)
		cur.execute(sql)
		conn.commit()
		sql = "delete from TEAM_WAIT where USER_ID = '%s'"%name
		cur.execute(sql)
		conn.commit()


	conn.close()

	return redirect(url_for('teams.teammanage'))
