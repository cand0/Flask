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
