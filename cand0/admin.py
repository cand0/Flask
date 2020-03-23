from flask import Flask, render_template, request, session, Blueprint, redirect, url_for, redirect
import sqlite3

admin = Blueprint('admin', __name__)

@admin.route('/admin/')
def admin_main():
	return render_template("admin.html")

@admin.route('/admin-challenges/')
def adminchallenge():
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

@admin.route('/admin-teams/')
@admin.route("/admin-teams/<name>")
def adminteam(name = None):
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
                                        option = 1;
                                        break;
                return render_template("admin-team.html",teams=teams, name = name, users = users, sel_team = sel_team[0], my_team = my_team, option = option)

        if 'ID' in session:
                return redirect(url_for('teams.adminteam', name = my_team[0][0]))
        else :
                return render_template("admin-team.html", teams=teams, option = option)
