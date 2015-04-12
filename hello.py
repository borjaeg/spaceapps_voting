from flask import Flask, render_template, redirect, url_for, session
from flaskext.mysql import MySQL
from flask import request


mysql = MySQL()
app = Flask(__name__)
app.debug = True
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'spaceapps'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def hello():
	return redirect("/login")

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/repeat")
def repeat():
	return render_template("repeat.html")

@app.route("/invalid")
def invalid():
	return render_template("invalid_email.html")

@app.route("/authenticate")
def authenticate():
	email = request.args.get('email', '')
	if email != "admin":
		cursor = mysql.connect().cursor()
		query = "SELECT email, hasVoted FROM participants WHERE email = '%s'" % email
		cursor.execute(query)
		data = cursor.fetchone()
		if data is None:
			return "-1"
		else:
			print data
			if data[1] == 0:
				session['email'] = email
				return "0"
			else: # the participant has voted
				return "-2"
	else:
		session['email'] = "admin"
		return "0"
		

@app.route("/projects")
def projects():
	cursor = mysql.connect().cursor()
	query = "SELECT id_project, hashtag FROM projects;"
	cursor.execute(query)
	projects = cursor.fetchall()
	return render_template("projects.html", projects = projects)

@app.route("/vote")
def vote():
	project = request.args.get('project', '')
	cursor = mysql.connect().cursor()
	query = "SET autocommit=1;"
	cursor.execute(query)
	query = "UPDATE projects SET num_votes = num_votes + 1 WHERE hashtag='%s';" % project
	cursor.execute(query)
	print session['email']
	query = "UPDATE participants SET hasVoted = 1, hashtag ='%s' WHERE email='%s';" % (project, session['email'])
	cursor.execute(query)

	return "0"

@app.route("/success")
def success():
	return render_template("success.html")

@app.route("/compute_winner")
def compute_winner():
	cursor = mysql.connect().cursor()
	query_votes = "SELECT hashtag, num_votes FROM projects;"
	cursor.execute(query_votes)
	votes = cursor.fetchall()
	rank = 1
	max_points = -1
	partial_winner = 'empty'
	for vote in votes:
		if vote[1] > max_points:
			partial_winner = vote[0]
			max_points = vote[1]

	return render_template("winner.html", winner = partial_winner)

if __name__ == "__main__":
	app.run()