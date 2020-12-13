######################################################3
#
#	Naming Scheme is as follows
#	ct - is related to covidtracking.com api
#	flDOH - is related to Florida Department of Health api
#	hhs - is related to healthdata.gov
#	cdc - is related to cdc
#
#
#
#
########################################################
import sqlite3 as sql
from buildUpdateDB import buildUpdateDB
from datetime import date, time
import calendar
import requests
import json

def runDataUpdate():
	#Set timezone here
	timezone = -5
	#Get the current day
	today = date.today()
	#Convert to epoch
	eDate = int(today.strftime("%s"))*1000
	eDate = eDate - (5+timezone)*3600000

	checkforUpdates()

def checkforUpdates():

	#Print message to console indicating start
	print ("Checking for Updates")
	#Connect to DB
	conn = sql.connect('covid_data.db')
	cur = conn.cursor()

	#Grab current highest patientID
	cur.execute("SELECT MAX(ObjectID) FROM Patients")
	newestPatient = (cur.fetchall())[0][0]
	

	#Build URL
	url = "https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/"\
	+ "rest/services/Florida_COVID19_Case_Line_Data_NEW/" \
	+ "FeatureServer/0/query?where=1%3D1&outFields=*&orderByFields" \
	+ "=ObjectID%20DESC&outSR=4326&f=json"

	#Fetch response and decode
	response = requests.get(url)
	r = json.loads(response.content.decode())

	#Grab latest entry object ID#
	data = r['features']
	output = data[0]['attributes']['ObjectId']
	print (output)
	print (newestPatient)
	if output > newestPatient:
		print("Updates Found, Building New DB")
		buildUpdateDB()
	else:
		print("Nothing to update at this time")


if __name__ == "__main__":
	runDataUpdate()
