import sqlite3 as sql
import requests


from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

#Index Page
@app.route('/')
def index():

	#Connect to DB
	conn = sql.connect('covid_data.db')
	#Setting row factor for dict values
	conn.row_factory = sql.Row
	cur = conn.cursor()
	cur.execute('SELECT SUM(Negative) AS Negative, SUM(Positive) AS Positive,\
		SUM(Total) AS Total FROM Totals')

	#Turn Sums into Dict for passing
	currentData = [dict(row) for row in cur.fetchall()]
	currentData = currentData[0]

	return render_template('index.html', currentData=currentData)


if __name__=="__main__":
	app.run(debug = True)
