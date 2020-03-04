from flask import Flask, render_template, url_for, request, redirect, session
import sqlite3


app = Flask(__name__)

app.secret_key = 'session_secret_key'

@app.route("/")
@app.route("/index")
def index():
	return render_template('index.html')

@app.route("/no-sidebar")
def nosidebar():
	return render_template('no-sidebar.html')

		###auth###
		#app.secret_key
@app.route("/sign-up")
def signup():
	return render_template('sign-up.html')

@app.route("/sign-up-proc", methods=['POST'])
def signupproc():
	ID = request.form['ID']
	PSW = request.form['PSW']
	member1 = request.form['member1']
	member2 = request.form['member2']
	member3 = request.form['member3']
	Score = 0
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()
	sql = "insert into TEAM(ID, PW, Member1, Member2, Member3, Score) values(?,?,?,?,?,?)"
	cur.execute(sql, (ID, PSW, member1, member2, member3, Score))

	conn.commit()
	conn.close()
	return redirect(url_for('index'))

@app.route("/sign-in")
def signin():
	if 'ID' in session:
		return "your session ID = " + str(session["ID"])
	else:
		return render_template('sign-in.html')

@app.route("/sign-in-proc", methods=['POST'])
def signinproc():
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()
	ID = request.form['ID']
	PW = request.form['PSW']
	cur.execute("select PW from TEAM where TEAM.ID='%s'"%ID)
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

@app.route("/logout")
def logout():
	session.pop('ID', None)
	return redirect(url_for('index'))


		###challenge###
@app.route("/challenge")
def challenge():
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	cur.execute("select NAME, CATEGORY, MESSAGE, VALUE from CHALLENGE")
	prob = cur.fetchall()

	cur.execute("select distinct CATEGORY from CHALLENGE")
	category=cur.fetchall()

	conn.close()

	return render_template("challenge.html", prob=prob, category=category)





@app.route("/test")
def test():
	test = 10
	return render_template("test.html", test=test)
#	return str(session["ID"])
@app.route("/test2")
def test2():
	return render_template("test2.html")
@app.route("/test3")
def test3():
	return render_template("test3.html")

#if __name__ == '__main__':
#	app.run(host="0.0.0.0", port="5000")
