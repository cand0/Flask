from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def index():
	return render_template('index.html')

@app.route("/login.html")
def login():
	return render_template('login.html')

@app.route("/no-sidebar.html")
def nosidebar():
	return render_template('no-sidebar.html')

#nosidebar -> ctf challenges page
#Dropdown remodeling to etc --- Rank, Member ...
#leftsidebar remodeling to sign in, sign on


if __name__ == '__main__':
	app.run(host="0.0.0.0", port="80")
