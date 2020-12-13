import sqlite3 as sql
from datetime import datetime

#Get total resident
def getTotalResident():

	#Connect to DB
	conn = sql.connect('covid_data.db')
	cur = conn.cursor()

	#Fetch Count of Residents
	cur.execute('SELECT COUNT(*) FROM Patient WHERE Jurisdiction != "Non-FL resident" ')
	rows = cur.fetchall()

	#Close Database Connection
	conn.close()

	#return Result
	return rows[0][0]

def getTotalNonResident():

	#Connect to DB
	conn = sql.connect('covid_data.db')
	cur = conn.cursor()

	#Fetch Count of NonResidents
	cur.execute('SELECT COUNT(*) FROM Patient WHERE Jurisdiction = "Non-FL resident" ')
	rows = cur.fetchall()

	#Close Database Connection
	conn.close()

	#Return Result
	print(rows[0][0])

def getTotalResidentOOS():

	#Connect to DB
	conn = sql.connect('covid_data.db')
	cur = conn.cursor()

	#Fetch Count of NonResidents
	cur.execute('SELECT COUNT(*) FROM Patient WHERE Jurisdiction = "Not diagnosed/isolated in FL" ')
	rows = cur.fetchall()

	#Close Database Connection
	conn.close()

	#Return Result
	print(rows[0][0])

def getDataFromToday():

	#Connect to DB
	conn = sql.connect('covid_data.db')
	cur = conn.cursor()

	#Fetch Count of NonResidents
	cur.execute('SELECT COUNT(*) FROM Patient WHERE Jurisdiction = "Not diagnosed/isolated in FL" ')
	rows = cur.fetchall()

	#Close Database Connection
	conn.close()

	#Return Result
	print(rows[0][0])


if __name__ == "__main__":
	getTotalResidentOOS()
