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
	#return dataRef
if __name__ == "__main__":
	flDOHTotals()
