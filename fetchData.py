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
import requests
import json

def flDOHTotals():

	#Print message to console indicating start
	print ("Fetching Daily Positive and Negative Tests")
	#Connect to DB
	conn = sql.connect('covid_data.db')
	cur = conn.cursor()
	
	#URL for DOH API of totals
	url = "https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/rest/services/state_daily_testing/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"

	#Fetch response and decode
	response = requests.get(url)
	r = json.loads(response.content.decode())

	#Grab latest entry
	data = r['features']
	#Grab Fields
	for entry in data:
	#Set fields to vars for entry in DB
		date = entry['attributes']['Date']
		neg = entry['attributes']['Negative']
		pos = entry['attributes']['Positive']
		tot = entry['attributes']['Total']

		cur.execute("INSERT OR IGNORE INTO Totals(DateEpoch, Negative, Positive, Total)\
		VALUES(?,?,?,?)",(date,neg,pos,tot))

		conn.commit()

	conn.close()
	print("Finished Daily Positive and Negative Tests")
	flDOHZips()

def flDOHZips():

	#Print message to console indicating start
	print ("Fetching Cases By Zip Code")
	#Connect to DB
	conn = sql.connect('covid_data.db')
	cur = conn.cursor()
	
	#URL for DOH API of totals
	url = "https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/rest/" \
	+ "services/Florida_Cases_Zips_COVID19/FeatureServer/0/query?where" \
	+ "=1%3D1&outFields=ZIP,Places,c_places,Cases_1,COUNTYNAME&return" \
	+ "Geometry=false&outSR=4326&f=json"

	#Fetch response and decode
	response = requests.get(url)
	r = json.loads(response.content.decode())

	#Grab latest entry
	data = r['features']
	#Grab Fields
	for entry in data:
	#Set fields to vars for entry in DB
		zip = entry['attributes']['ZIP']
		places = entry['attributes']['Places']
		placesReport = entry['attributes']['c_places']
		num = entry['attributes']['Cases_1']
		county = entry['attributes']['COUNTYNAME']
		

		cur.execute("INSERT OR IGNORE INTO Zips(ZipCode,County,Places,\
		PlacesReport, NumberCases) VALUES(?,?,?,?,?)",\
		(zip,places,placesReport,num,county))

		conn.commit()

	conn.close()
	print("Finished ZipCodes")
	flDOHPatients()

def flDOHPatients():

	#Print message to console indicating start
	print("Fetching All Patient information")

	#Connect to DB
	conn = sql.connect('covid_data.db')
	cur = conn.cursor()

	#Set flag for determing if done running
	flag = True

	#Starting point
	start = -1

	while flag == True:
		#Build URL
		url = "https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/rest/services/" \
		+ "Florida_COVID19_Case_Line_Data_NEW/FeatureServer/0/query?where=ObjectId%20%3E%3D%20" \
		+ str(start+1) + "%20AND%20ObjectId%20%3C%3D%20" + str(start+2000) \
		+ "&outFields=*&outSR=4326&f=json"
	
		#Fetch response and decode
		response = requests.get(url)
		r = json.loads(response.content.decode())

		#Grab latest entry
		data = r['features']
		print ("Starting batch " + str(start+1))
		#If results are empty, end search, else increment start for next batch
		if not data:
			flag = False
		else:
			start += 2000
			
		#Grab Fields
		for entry in data:
			#Set fields to vars for entry in DB
			county = entry['attributes']['County']
			age = entry['attributes']['Age']
			ageGroup = entry['attributes']['Age_group']
			gender = entry['attributes']['Gender']
			jurisdiction = entry['attributes']['Jurisdiction']
			travel = entry['attributes']['Travel_related']
			origin = entry['attributes']['Origin']
			edVisit = entry['attributes']['EDvisit']
			hospital = entry['attributes']['Hospitalized']
			died = entry['attributes']['Died']
			caseStatus = entry['attributes']['Case_']
			contact = entry['attributes']['Contact']
			caseDate = entry['attributes']['Case1']
			eventDate = entry['attributes']['EventDate']
			chartDate = entry['attributes']['ChartDate']
			objectID = entry['attributes']['ObjectId']
			county = entry['attributes']['County']

			cur.execute("INSERT OR REPLACE INTO Patients(ObjectID,\
			Age, age_group, Gender, Jurisdiction, Travel_related,\
			Origin, EDVisit, Hospitalized, Died, CaseStatus,\
			Contact, CaseDate, EventDate, ChartDate, County)\
			VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
			(objectID,age,ageGroup,gender,jurisdiction,travel,origin,\
			edVisit,hospital,died,caseStatus,contact,caseDate,\
			eventDate,chartDate,county))

			conn.commit()

	#Print message to console indicating start
	print("Finished All Patient information")
	
	conn.close()



if __name__ == "__main__":
	flDOHTotals()
