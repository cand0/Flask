from flask import Flask, render_template, request, session, Blueprint, redirect, url_for, redirect
import sqlite3



admin = Blueprint('admin', __name__)

#index
@admin.route('/admin/')
def admin_main():
	if 'admin' not in session:
		return redirect(url_for('admin.adminpw'))

	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	cur.execute("select NUM, NAME, MESSAGE from HINT")
	hints = cur.fetchall()

	return render_template("admin.html", hints = hints)

#hint
@admin.route('/admin-hint-proc/', methods = ["POST"])
def admin_hint():
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	submit = request.form['submit']

	if submit == "Create":
		name = request.form['name']
		message = request.form['message']

		sql = "insert into HINT(NAME, MESSAGE) values(?,?)"
		cur.execute(sql, (name, message))
		conn.commit()
	elif submit == "Modify":
		num = request.form['num']
		name = request.form['name'+num]
		message = request.form['message'+num]

		sql = "update HINT set name = '%s', message = '%s' where num = '%s'"%(name, message, num)
		cur.execute(sql)
		conn.commit()
	elif submit == "Delete":
		num = request.form['num']

		sql = "delete from HINT where num = '%s'"%(num)
		cur.execute(sql)
		conn.commit()

	conn.close()
	return redirect(url_for('admin.admin_main'))

#admin-password
@admin.route('/admin-pw/')
def adminpw():
	return render_template("admin-pw.html")

@admin.route('/admin-pw-proc/', methods=['POST'])
def adminpwproc():
	ID = request.form['ID']
	PW = request.form['PW']

	if ID == "admin":
		if PW == "admin_pw":
			session['admin'] = ID
			return redirect(url_for('admin.admin_main'))
	return '''<script>alert("Permission Denied");history.go(-1);</script>'''

#challenge
@admin.route('/admin-challenges/')
def adminchallenge():
	if 'admin' not in session:
		return redirect(url_for('admin.adminpw'))

	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	cur.execute("select NAME, CATEGORY, MESSAGE, VALUE from CHALLENGE")
	prob = cur.fetchall()
	prob_len = len(prob)

	cur.execute("select distinct CATEGORY from CHALLENGE")
	category=cur.fetchall()

	conn.close()

	return render_template("admin-challenges.html", prob=prob, prob_len = prob_len ,category=category)

@admin.route('/admin-challenges-auth/', methods=['POST'])
def adminchallengeauth():
	if 'admin' not in session:
		return redirect(url_for('admin.adminpw'))

	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	name = request.form['challenge_name']
	category = request.form['challenge_category'].upper()
	message = request.form['challenge_message']
	value = request.form['challenge_value']
	flag = request.form['challenge_flag']

	sql = "insert into CHALLENGE(NAME, CATEGORY, MESSAGE, VALUE, FLAG) values(?,?,?,?,?)"
	cur.execute(sql, (name, category, message, value, flag))
	conn.commit()
	conn.close()
	return redirect(url_for('admin.adminchallenge'))

@admin.route('/admin-challenges-fix/', methods=['POST'])
def adminchallengesfix():
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	name = request.form['admin_challenge_name']
	value = request.form['admin_challenge_value']
	message = request.form['admin_challenge_message']
	category = request.form['admin_challenge_category']
	submit = request.form['submit']

	if submit == "update" :
		sql = "update CHALLENGE set VALUE = '%s', MESSAGE = '%s', CATEGORY = '%s' where NAME = '%s'"%(value, message, category, name)
	elif submit == "delete" :
		sql = "delete from CHALLENGE where NAME = '%s'"%(name)
	cur.execute(sql)
	conn.commit()
	conn.close()
	return redirect(url_for('admin.adminchallenge'))

#team
@admin.route('/admin-teams/')
@admin.route("/admin-teams/<name>")
def adminteam(name = None):
	if 'admin' not in session:
		return redirect(url_for('admin.adminpw'))

	option = 0;

	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	#find team list
	cur.execute("select NAME from TEAM")
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

		#Modify My Team
		option = 0
		for chk_user in users:
			if 'ID' in session:
				if chk_user[0] == session['ID'] :
					option = 1
					break
		return render_template("admin-team.html",teams=teams, name = name, users = users, sel_team = sel_team[0], my_team = my_team, option = option)

	if 'ID' in session:
		return redirect(url_for('teams.adminteam', name = my_team[0][0]))
	else :
		return render_template("admin-team.html", teams=teams, option = option)

@admin.route('/admin-teams-proc/<name>')
def adminteamproc(name = None):
	if 'admin' not in session:
		return redirect(url_for('admin.adminpw'))

	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	#delete team and user
	sql = "delete from USER where ID in (select ID from user where TEAM_NAME in (select NAME from team where name = '%s'))"%(name)
	cur.execute(sql)
	conn.commit()

	sql = "delete from TEAM where NAME = '%s'"%(name)
	cur.execute(sql)
	conn.commit()

	conn.close()
	return '''<script>alert("success");window.location.href="/admin-teams";;</script>'''

@admin.route('/admin-user-proc/<name>')
def adminuserproc(name = None):
	if 'admin' not in session:
		return redirect(url_for('admn.adminpw'))

	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	#delte user
	sql = "delete from user where ID = '%s'"%(name)
	cur.execute(sql)
	conn.commit()

	conn.close()
	return '''<script>alert("success");window.location.href="/admin-teams";;</script>'''
