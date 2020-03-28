from flask import Flask, render_template, url_for, request, redirect, session, escape, Blueprint
import sqlite3

auth = Blueprint('auth', __name__)


@auth.route("/sign-up/")
def signup():
        placeholder_signup = "이름 : \n이메일 : "
        return render_template('sign-up.html', placeholder_signup = placeholder_signup)

@auth.route("/sign-up-proc/", methods=['POST'])
def signupproc():
	ID = request.form['ID']
	PSW = request.form['PSW']
	PSW_repeat = request.form['PSW_repeat']
	TEAM_NAME = request.form['TEAM_NAME']
	MESSAGE = request.form['MESSAGE']

	if PSW == PSW_repeat:
		conn = sqlite3.connect('/cand0/cand0/cand0.db')
		cur = conn.cursor()

		cur.execute("select NAME from TEAM where NAME = '%s'"%TEAM_NAME)
		chk_team = cur.fetchall()

			###user TEAM insert###
		if chk_team == []:
			sql = "insert into TEAM(NAME, LEADER) values(?,?)"
			cur.execute(sql, (TEAM_NAME, ID))
			conn.commit()
		sql = "insert into USER values(?,?,?,?)"
		cur.execute(sql, (ID, PSW, TEAM_NAME, MESSAGE))
		conn.commit()

		conn.close()
		return redirect(url_for('index'))
	else :
		return '''<script>alert("Passwords do not match.");history.go(-1);</script>'''

@auth.route("/sign-in/")
def signin():
        if 'ID' in session:
                return "your session ID = " + str(session["ID"])
        else:
                return render_template('sign-in.html')

@auth.route("/sign-in-proc/", methods=['POST'])
def signinproc():
        conn = sqlite3.connect('/cand0/cand0/cand0.db')
        cur = conn.cursor()
        ID = request.form['ID']
        PW = request.form['PSW']
        cur.execute("select PW from USER where USER.ID='%s'"%ID)
        rows = cur.fetchall()
        conn.close()

        if rows:
                if str(PW) == str(rows[0][0]):
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

