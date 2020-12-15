import sqlite3 as sql
import requests
from parseData import getPos30, getDeaths30, getPrevDay


from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

#Index Page
@app.route('/')
def index():

	#Connect to DB
	conn = sql.connect('quickAccess.db')
	#Setting row factor for dict values
	conn.row_factory = sql.Row
	cur = conn.cursor()
	cur.execute('SELECT * FROM Quick ORDER BY Total DESC')

	#Turn Sums into Dict for passing
	currentData = [dict(row) for row in cur.fetchall()]
	currentData = currentData[0]

	#Get Resident positives from last 30 days
	res30 = getPos30() 
	deaths30 = getDeaths30()

	return render_template('index.html', currentData=currentData, res30=res30, \
		deaths30=deaths30)

#Index Page
@app.route('/dailyBreakdown')
def dailyBreak():

	#Connect to DB
	conn = sql.connect('quickAccess.db')
	#Setting row factor for dict values
	conn.row_factory = sql.Row
	cur = conn.cursor()
	cur.execute('SELECT * FROM Quick ORDER BY Total DESC')

	#Turn Sums into Dict for passing
	currentData = [dict(row) for row in cur.fetchall()]
	currentData = currentData[0]

	#Get Resident positives from last 30 days
	dayData = getPrevDay() 

	return render_template('dailyBreakdown.html', currentData=currentData, dayData=dayData)


if __name__=="__main__":
	app.run(debug = True)
