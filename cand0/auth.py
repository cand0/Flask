from flask import Flask, render_template, url_for, request, redirect, session, escape, Blueprint
import sqlite3

import bcrypt



auth = Blueprint('auth', __name__)


@auth.route("/sign-up-proc/", methods=['POST'])
def signupproc():
	ID = request.form['ID']
	PSW = request.form['PSW']
	PSW_repeat = request.form['PSW_repeat']
	TEAM_NAME = request.form['TEAM_NAME']
	MESSAGE = request.form['MESSAGE']

	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	if PSW == PSW_repeat:
		cur.execute("select NAME from TEAM where NAME = '%s'"%TEAM_NAME)
		chk_team = cur.fetchall()

			###user TEAM insert###
		#team not exist
		if chk_team == []:
			sql = "insert into TEAM(NAME, LEADER) values(?,?)"
			cur.execute(sql, (TEAM_NAME, ID))
			conn.commit()
		#team exist
		else :
			sql = "insert into TEAM_WAIT(USER_ID, TEAM_ID) values(?,?)"
			cur.execute(sql, (ID, TEAM_NAME))
			conn.commit()
			TEAM_NAME = "WAIT_TEAM"
		#password encryption
		hash_password = bcrypt.hashpw(PSW.encode(), bcrypt.gensalt())

		sql = "insert into USER(ID, PW, TEAM_NAME, MESSAGE) values(?,?,?,?)"
		cur.execute(sql, (ID, hash_password, TEAM_NAME, MESSAGE))
		conn.commit()

		conn.close()
		return redirect(url_for('index'))
	else :
		return '''<script>alert("Passwords do not match.");history.go(-1);</script>'''

@auth.route("/sign-in-proc/", methods=['POST'])
def signinproc():
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()
	ID = request.form['ID']
	PW = request.form['PSW']

	cur.execute("select PW from USER where USER.ID='%s'"%ID)
	rows = cur.fetchall()
	conn.close()

	#check password
	if rows:
		if bcrypt.checkpw(PW.encode(), rows[0][0]):
			session['ID'] = request.form['ID']
			return redirect(url_for('index'))
		else :
			return "password incorrect"
	else :
		return "no ID"

@auth.route("/logout/")
def logout():
        session.pop('ID', None)
        return redirect(url_for('index'))

