
from flask import Flask, render_template, url_for, request, redirect, session, escape, Blueprint
import sqlite3

challenges = Blueprint('challenges', __name__)

@challenges.route('/challenges/')
def challengess():
       conn = sqlite3.connect('/cand0/cand0/cand0.db')
       cur = conn.cursor()

       cur.execute("select NAME, CATEGORY, MESSAGE, VALUE from CHALLENGE")
       prob = cur.fetchall()

       cur.execute("select distinct CATEGORY from CHALLENGE")
       category=cur.fetchall()

       conn.close()

       return render_template("challenge.html", prob=prob, category=category)

