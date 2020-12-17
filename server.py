import sqlite3 as sql
import requests
from parseData import getPos30, getDeaths30, getPrevDay,getPrevDayCounty
from parseData import getPrevRangeCounty, getPrevRangeState
from parseData import getAllState, getAllCounty
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

#Daily Breakdown Page
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

#Daily County Page
@app.route('/daily/<county>')
def dailyCounty(county):

	#Connect to DB
	conn = sql.connect('quickAccess.db')
	#Setting row factor for dict values
	conn.row_factory = sql.Row
	cur = conn.cursor()
	cur.execute('SELECT * FROM Quick ORDER BY Total DESC')

	#Turn Sums into Dict for passing
	currentData = [dict(row) for row in cur.fetchall()]
	currentData = currentData[0]

	trimCounty = county.replace("%20", " ")
	#Get Resident positives from last 30 days
	dayData = getPrevDayCounty(trimCounty) 

	return render_template('dailyCounty.html', currentData=currentData, dayData=dayData)

#Daily County Page
@app.route('/<num>day/<county>')
def rangeCounty(num,county):

	#Connect to DB
	conn = sql.connect('quickAccess.db')
	#Setting row factor for dict values
	conn.row_factory = sql.Row
	cur = conn.cursor()
	cur.execute('SELECT * FROM Quick ORDER BY Total DESC')

	#Turn Sums into Dict for passing
	currentData = [dict(row) for row in cur.fetchall()]
	currentData = currentData[0]

	trimCounty = county.replace("%20", " ")

	#Get Resident positives from last 30 days
	if county != "State":
		dayData = getPrevRangeCounty(trimCounty,num) 
	else:
		dayData = getPrevRangeState(num)

	return render_template('rangeCounty.html', currentData=currentData, \
		dayData=dayData, days=num)

#Daily County Page
@app.route('/all/<county>')
def allCounty(county):

	#Connect to DB
	conn = sql.connect('quickAccess.db')
	#Setting row factor for dict values
	conn.row_factory = sql.Row
	cur = conn.cursor()
	cur.execute('SELECT * FROM Quick ORDER BY Total DESC')

	#Turn Sums into Dict for passing
	currentData = [dict(row) for row in cur.fetchall()]
	currentData = currentData[0]

	trimCounty = county.replace("%20", " ")

	#Get Resident positives from last 30 days
	if county != "State":
		dayData = getAllCounty(trimCounty) 
	else:
		dayData = getAllState()

	return render_template('allCounty.html', currentData=currentData, \
		dayData=dayData)

if __name__=="__main__":
	app.run(debug = True)
