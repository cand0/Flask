from flask import Flask, render_template

from cand0.challenges import challenges
from cand0.auth import auth
from cand0.teams import teams

app = Flask(__name__)

app.secret_key = 'session_secret_key'

@app.route("/")
@app.route("/index/")
def index():
        return render_template('index.html')
@app.route("/test/")
@app.route("/test.html/")
def test():
	return render_template('test.html')

app.register_blueprint(challenges)
app.register_blueprint(auth)
app.register_blueprint(teams)
