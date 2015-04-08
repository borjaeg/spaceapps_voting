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
	cursor = mysql.connect().cursor()
	query = "SELECT * FROM participants WHERE email = '%s'" % email
	cursor.execute(query)
	data = cursor.fetchone()
	if data is None:
		return "-1"
	else:
		print data
		if data[2] == 0:
			session['email'] = email
			return "0"
		else: # the participant has voted
			return "-2"
		

@app.route("/projects")
def projects():
	cursor = mysql.connect().cursor()
	query = "SELECT id_project, hashtag, team FROM projects;"
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


def coca_colapps_formule(total_votes, num_projects, rank):
	return int((total_votes/(num_projects/2))/rank)

@app.route("/compute_winner")
def compute_winner():
	cursor = mysql.connect().cursor()
	query_total_votes = "SELECT SUM(num_votes) AS total_votos FROM projects;"
	cursor.execute(query_total_votes)
	total_votes = cursor.fetchone()[0]
	print type(total_votes)
	query_num_projects = "SELECT COUNT(*) AS num_projects FROM projects;"
	cursor.execute(query_num_projects)
	num_projects = cursor.fetchone()[0]
	query_votes_by_project = "SELECT hashtag, num_votes, social_votes FROM projects ORDER BY social_votes DESC;"
	cursor.execute(query_votes_by_project)
	votes_by_project = cursor.fetchall()
	rank = 1
	projects = []
	for votes in votes_by_project:
		social_points = coca_colapps_formule(total_votes, num_projects, rank)
		rank = rank + 1
		projects.append((votes[0], social_points + votes[1]))
		print votes[0]
		print social_points + votes[1]

	max_points = -1
	partial_winner = 'empty'
	for project in projects:
		print project[1]
		if project[1] > max_points:
			partial_winner = project[0]
			max_points = project[1]

	return render_template("winner.html", winner = partial_winner)

if __name__ == "__main__":
	app.run()