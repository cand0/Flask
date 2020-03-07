from flask import Flask, render_template, url_for, request, redirect, session, escape
import sqlite3


app = Flask(__name__)

app.secret_key = 'session_secret_key'

@app.route("/")
@app.route("/index/")
def index():
	return render_template('index.html')

@app.route("/no-sidebar/")
def nosidebar():
	return render_template('no-sidebar.html')

		###auth###
		#app.secret_key
@app.route("/sign-up/")
def signup():
	return render_template('sign-up.html')

@app.route("/sign-up-proc/", methods=['POST'])
def signupproc():
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	ID = request.form['ID']
	PSW = request.form['PSW']
	TEAM_NAME = request.form['TEAM_NAME']
	MESSAGE = request.form['MESSAGE']

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

@app.route("/sign-in/")
def signin():
	if 'ID' in session:
		return "your session ID = " + str(session["ID"])
	else:
		return render_template('sign-in.html')

@app.route("/sign-in-proc/", methods=['POST'])
def signinproc():
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()
	ID = request.form['ID']
	PW = request.form['PSW']
	cur.execute("select PW from USER where USER.ID='%s'"%ID)
	rows = cur.fetchall()
	conn.close()

	if rows:
		if PW == rows[0][0]:
			session['ID'] = request.form['ID']
			return redirect(url_for('index'))
		else :
			return "password incorrect"
	else :
		return "no ID"

@app.route("/logout/")
def logout():
	session.pop('ID', None)
	return redirect(url_for('index'))

		###TEAM###
@app.route("/team/")
@app.route("/team/<name>")
def team(name = None):
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	#find team list
	cur.execute("select NAME, LEADER, SCORE from TEAM")
	teams = cur.fetchall()

	if name != None:
		cur.execute("select ID, MESSAGE from USER where TEAM_NAME='%s'"%name)
		users = cur.fetchall()

		#select team information
		cur.execute("select TEAM_NAME from USER where ID='%s'"%name)
		my_team = cur.fetchall()
		cur.execute("select NAME, LEADER, SCORE from TEAM where NAME='%s'"%my_team[0][0])
		my_team = cur.fetchall()

		return render_template("team.html",teams=teams , name = name, users = users, my_team = my_team[0])
	return render_template("team.html", teams=teams)

		###challenge###
@app.route("/challenge/")
def challenge():
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	cur.execute("select NAME, CATEGORY, MESSAGE, VALUE from CHALLENGE")
	prob = cur.fetchall()

	cur.execute("select distinct CATEGORY from CHALLENGE")
	category=cur.fetchall()

	conn.close()

	return render_template("challenge.html", prob=prob, category=category)




#test zone
@app.route("/test")
def test():
	test = 10
	return render_template("test.html", test=test)
#	return str(session["ID"])
@app.route("/test2/")
@app.route("/test2/<name>")
def test2(name):
	return 'welcome' + session['ID']
@app.route("/test3")
def test3():
	return render_template("test3.html")

@app.route("/profile/<username>")
def get_profile(username):
	return "profile: " + escape(username)

if __name__ == '__main__':
	app.run(host="0.0.0.0", port="5000")
