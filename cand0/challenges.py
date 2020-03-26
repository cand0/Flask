from flask import Flask, render_template, url_for, request, redirect, session, escape, Blueprint
import sqlite3

challenges = Blueprint('challenges', __name__)

@challenges.route('/challenges/')
def challenge():
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	cur.execute("select NAME, CATEGORY, MESSAGE, VALUE from CHALLENGE")
	prob = cur.fetchall()
	prob_len = len(prob)

	cur.execute("select distinct CATEGORY from CHALLENGE")
	category=cur.fetchall()

	conn.close()

	return render_template("challenge.html", prob=prob, prob_len = prob_len ,category=category)

@challenges.route('/challenges-auth/', methods=['POST'])
def challengesauth():
	conn = sqlite3.connect('/cand0/cand0/cand0.db')
	cur = conn.cursor()

	#Get Parameter Flag
	FLAG = request.form['test']

	cur.execute("select NAME, VALUE from CHALLENGE where FLAG = '%s'"%FLAG)
	chk_flag = cur.fetchall()

	#Flag -> correct or incorrect
	if chk_flag == []:
		conn.close()
		return "No Flag"
	else:
		#Get User Team Name
		cur.execute("select TEAM_NAME from USER where ID = '%s'"%session['ID'])
		USER_TEAM_NAME = cur.fetchall()
		#duplicate Flag authentication
		cur.execute("select USER_TEAM_NAME, CHALLENGE_NAME from SOLVES where CHALLENGE_NAME = '" + str(chk_flag[0][0]) + "' and USER_TEAM_NAME = '%s'"%USER_TEAM_NAME[0][0])
		dup_auth = cur.fetchall()

		if dup_auth == []:

			#insert solves
			sql = "insert into SOLVES(USER_TEAM_NAME, USER_ID, CHALLENGE_NAME) VALUES (?, ?, ?)"
			cur.execute(sql, (USER_TEAM_NAME[0][0], session['ID'], str(chk_flag[0][0])))
			conn.commit()

			#insert team score++
#			sql = "update TEAM SET SCORE = SCORE + " + str(chk_flag[0][1]) + " where TEAM.NAME = '%s'"%USER_TEAM_NAME[0][0]
			sql = "UPDATE TEAM SET SCORE = SCORE + '%s', AUTH_TIME = (DATETIME('NOW')) WHERE TEAM.NAME = '%s'"%(str(chk_flag[0][1]), USER_TEAM_NAME[0][0])
			cur.execute(sql)
			conn.commit()

			conn.close()
			return "SUCCES " + str(chk_flag[0][0]) + " !!!!" + session['ID']
		else :
			return "duplicate authentication"
