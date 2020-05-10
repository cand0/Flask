from flask import Flask, render_template, request, session, Blueprint, redirect, url_for, redirect
import sqlite3

#file upload/download
from werkzeug import secure_filename
from flask import send_from_directory

import os

#password encryption
import bcrypt




admin = Blueprint('admin', __name__)

#admin-password
@admin.route('/admin-pw/')
def adminpw():
	return render_template("admin-pw.html")

@admin.route('/admin-pw-proc/', methods=['POST'])
def adminpwproc():
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	ID = request.form['ID']
	PW = request.form['PW']

	cur.execute("select PW from USER where ID = 'admin'")
	password = cur.fetchall()
	conn.close()

	if ID == "admin" :
		if bcrypt.checkpw(PW.encode(), password[0][0]):
			session['admin'] = ID
			return redirect(url_for('admin.admin_main'))
	return '''<script>alert("Permission Denied");history.go(-1);</script>'''

#index
@admin.route('/admin/')
def admin_main():
	if 'admin' not in session:
		return redirect(url_for('admin.adminpw'))

	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	cur.execute("select NUM, NAME, MESSAGE from HINT")
	hints = cur.fetchall()

	conn.close()

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

#challenge
@admin.route('/admin-challenges/')
def adminchallenge():
	if 'admin' not in session:
		return redirect(url_for('admin.adminpw'))

	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	cur.execute("select NAME, CATEGORY, MESSAGE, VALUE, FLAG from CHALLENGE")
	prob = cur.fetchall()
	prob_len = len(prob)

	cur.execute("select distinct CATEGORY from CHALLENGE")
	category=cur.fetchall()

	conn.close()

	return render_template("admin-challenges.html", prob=prob, prob_len = prob_len ,category=category)

@admin.route('/admin-challenges-create/', methods=['POST'])
def adminchallengescreate():
	if 'admin' not in session:
		return redirect(url_for('admin.adminpw'))

	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	name = request.form['challenge_name']
	category = request.form['challenge_category'].upper()
	message = request.form['challenge_message']
	value = request.form['challenge_value']
	flag = request.form['challenge_flag']

	#deduplication name or flag
	cur.execute("select NAME from CHALLENGE where FLAG = '%s' or NAME = '%s'"%(flag,name))
	duplication_value = cur.fetchall()

	if duplication_value != []:
		return "duplication with " + str(duplication_value)

	sql = "insert into CHALLENGE(NAME, CATEGORY, MESSAGE, VALUE, FLAG) values(?,?,?,?,?)"
	cur.execute(sql, (name, category, message, value, flag))
	conn.commit()
	conn.close()
	return redirect(url_for('admin.adminchallenge'))

@admin.route('/admin-challenges-fix/', methods=['POST'])
def adminchallengesfix():
	if 'admin' not in session:
		return redirect(url_for('admin.adminpw'))
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	name = request.form['admin_challenge_name']
	value = request.form['admin_challenge_value']
	message = request.form['admin_challenge_message']
	category = request.form['admin_challenge_category']
	flag = request.form['admin_challenge_flag']
	submit = request.form['submit']

	if submit == "update" :
		#deduplication flag
		cur.execute("select NAME from CHALLENGE where FLAG = '%s'"%flag)
		duplication_flag = cur.fetchall()

		if duplication_flag != []:
			return "duplication flag with " + str(duplication_flag)

		sql = "update CHALLENGE set VALUE = '%s', MESSAGE = '%s', CATEGORY = '%s', FLAG = '%s' where NAME = '%s'"%(value, message, category, flag, name)
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
	cur.execute("select NAME, HIDDEN from TEAM")
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
		return redirect(url_for('admin.adminteam', name = my_team[0][0]))
	else :
		return render_template("admin-team.html", teams=teams, option = option)

@admin.route('/admin-teams-proc')
@admin.route('/admin-teams-proc/<type>/<name>')
def adminteamproc(type = None, name = None):
	if 'admin' not in session:
		return redirect(url_for('admin.adminpw'))

	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	if type == "delete":
		#delete team and user
		sql = "delete from USER where ID in (select ID from user where TEAM_NAME in (select NAME from team where name = '%s'))"%(name)
		cur.execute(sql)
		conn.commit()

		sql = "delete from TEAM where NAME = '%s'"%(name)
		cur.execute(sql)
		conn.commit()
		return '''<script>alert("delete success");window.location.href="/admin-teams";;</script>'''
	elif type == "hidden":
		cur.execute("select HIDDEN from TEAM where NAME = '%s'"%name)
		chk_hidden = cur.fetchall()

		if chk_hidden[0][0] == 0:
			val_hidden = 1
		elif chk_hidden[0][0] == 1:
			val_hidden = 0
		else :
			return "error check hidden value"
		cur.execute("update TEAM set HIDDEN = '%s' where name = '%s'"%(val_hidden, name))
		conn.commit()
		return '''<script>alert("hidden value change");window.location.href="/admin-teams";;</script>'''
	conn.close()
	return "error"

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
	return '''<script>alert("success");window.location.href="/admin-teams";</script>'''

@admin.route('/admin-files/')
def adminfiles():
	if 'admin' not in session:
		return redirect(url_for('admin.adminpw'))

	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()
	cur.execute("select FIELD, NAME from FILES");
	files = cur.fetchall();

	cur.execute("select distinct CATEGORY from CHALLENGE");
	challenges_category = cur.fetchall();

	conn.close()
	return render_template("admin-files.html", files = files, len_files = len(files), challenges_category = challenges_category)

@admin.route("/admin-files-proc/")
@admin.route("/admin-files-proc/<name>/")
@admin.route("/admin-files-proc/", methods = ['GET', 'POST'])
def adminfilesproc(name = None):
	if 'admin' not in session:
		return redirect(url_for('admin.adminpw'))

	if request.method == 'POST':
		conn = sqlite3.connect('/cand0/cand0/cand0.db')
		cur = conn.cursor()

		field = request.form['field']
		f = request.files['file']

		cur.execute("select NAME from FILES where NAME = '%s'"%f.filename)
		chk_filename = cur.fetchall()
		if chk_filename == []:	#no file
			f.save("/cand0/cand0/files/" + secure_filename(f.filename))
			cur.execute("insert into FILES(field, NAME) values(?,?)", (field, f.filename))
			conn.commit()
			conn.close()
			return '''<script>alert("success");window.location.href="/admin-files";</script>'''
		else :
			conn.close()
			return "Check File Name"
	else :
		if name != None:
			conn = sqlite3.connect('/cand0/cand0/cand0.db')
			cur = conn.cursor()

			cur.execute("delete from FILES where NAME = '%s'"%name)
			conn.commit()
			conn.close()

			os.system("rm /cand0/cand0/files/" + name)
			return '''<script>alert("success");window.location.href="/admin-files";</script>'''
		return '''<script>alert("error");window.location.href="/admin-files";</script>'''
