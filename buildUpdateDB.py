import sqlite3 as sql
import requests
import json
import os
from datetime import date,time
import calendar
from fetchVaccine import fetchVaccine

def buildUpdateDB():

	conn = sql.connect('covid_update.db')

	conn.execute("CREATE TABLE Patients(ObjectID INT," \
		+"County TEXT,"\
		+"Age INT,"\
		+"Age_group TEXT,"\
		+"Gender TEXT,"\
		+"Jurisdiction TEXT,"\
		+"Travel_related TEXT,"\
		+"Origin TEXT,"\
		+"EDVisit TEXT,"\
		+"Hospitalized TEXT,"\
		+"Died TEXT,"\
		+"CaseStatus TEXT,"\
		+"Contact TEXT,"\
		+"CaseDate INT,"\
		+"EventDate INT,"\
		+"ChartDate INT,"\
		+"PRIMARY KEY (ObjectID))")

	conn.execute("CREATE TABLE Zips(ZipCode TEXT,"\
		+"County TEXT,"\
		+"Places TEXT,"\
		+"PlacesReport TEXT,"\
		+"NumberCases,"\
		+"PRIMARY KEY(ZipCode))")

	conn.execute("CREATE TABLE Totals (DateEpoch INT,"\
		+"Negative INT,"\
		+"Positive INT,"\
		+"Total INT,"\
		+"PRIMARY KEY (DateEpoch))")

	conn.close()
	flDOHTotals()

def flDOHTotals():

	#Print message to console indicating start
	print ("Fetching Daily Positive and Negative Tests")
	#Connect to DB
	conn = sql.connect('covid_update.db')
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
	conn = sql.connect('covid_update.db')
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
	conn = sql.connect('covid_update.db')
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
	updateQuick()

def updateQuick():

	#Print message to console indicating start
	print("Building Quick Info DB")

	#Connect to updated database
	#conn = sql.connect('covid_data.db')
	conn = sql.connect('covid_update.db')
	cur = conn.cursor()
	#Start series of slower queries to update quick access db for speed

	#Get Total Positive People in State
	cur.execute("SELECT COUNT(*) FROM Patients")
	total = (cur.fetchall())[0][0]
	print (total)

	#Get Total Positive Residents in State
	cur.execute("SELECT COUNT(*) FROM Patients WHERE Jurisdiction != 'Non-FL resident'")
	res = (cur.fetchall())[0][0]

	#Get Total Positive NonResidents in State
	cur.execute("SELECT COUNT(*) FROM Patients WHERE Jurisdiction = 'Non-FL resident'")
	non = (cur.fetchall())[0][0]

	#Get Total Positive Residents in State Hospitalized
	cur.execute("SELECT COUNT(*) FROM Patients WHERE "\
	+ "Jurisdiction != 'Non-FL resident' AND Hospitalized = 'YES'")
	reshosp = (cur.fetchall())[0][0]

	#Get Total Positive NonResidents in State Hospitalized
	cur.execute("SELECT COUNT(*) FROM Patients WHERE "\
	+ "Jurisdiction = 'Non-FL resident' AND Hospitalized = 'YES'")
	nonhosp = (cur.fetchall())[0][0]

	#Death values are Yes, NA, and Recent. For this it's best to use !NA for yes

	#Get Total	Residents in State Death
	cur.execute("SELECT COUNT(*) FROM Patients WHERE "\
	+ "Jurisdiction != 'Non-FL resident' AND Died != 'NA'")
	resdeath = (cur.fetchall())[0][0]

	#Get Total NonResidents in State Death
	cur.execute("SELECT COUNT(*) FROM Patients WHERE "\
	+ "Jurisdiction = 'Non-FL resident' AND Died != 'NA'")
	nondeath = (cur.fetchall())[0][0]

	conn.close()

	#Open quick DB to write values
	conn = sql.connect('quickAccess.db')
	cur = conn.cursor()

	cur.execute("INSERT OR REPLACE INTO Quick(Total,\
	Resident,NonResident,ResHosp,NonResHosp,ResDeath,NonResDeath,TimeStamp) \
	VALUES(?,?,?,?,?,?,?,datetime('now'))",\
	(total,res,non,reshosp,nonhosp,resdeath,nondeath))

	conn.commit()
	conn.close()

	#Go swap old db with new
	replaceDatabase()

def replaceDatabase():

	#Archive old DB and replace with new
	today = str(date.today())
	#Retry until avaliable
	while os.path.exists("covid_data.db"):
		os.rename('covid_data.db',"covid_data"+today+".db")

	#Rename new DB to old
	os.rename('covid_update.db','covid_data.db')
	updateCounty()

def updateCounty():

	#set Teimzone here
	timezone = -5
	#get the current day
	today = date.today()
	#Convert to epoch
	eDate = int(today.strftime("%s"))*1000
	eDate = eDate - (5+timezone)*3600000

	#Connect to DB
	conn = sql.connect("County.db")
	cur = conn.cursor()

	#Fetch new info
	url = "https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/arcgis/" \
	+ "rest/services/Florida_COVID19_Cases/FeatureServer/0/query?" \
	+ "where=1%3D1&outFields=*&outSR=4326&f=json"
	
	response = requests.get(url)
	r = json.loads(response.content.decode())

	#Grab entries
	data = r['features']

	for entry in data:

		input = entry['attributes']
		
		cur.execute('INSERT OR REPLACE INTO County(DateStamp,OBJECTID_12_13, \
		DEPCODE,COUNTYNAME,County,State,T_Total_Res,C_Female,C_Male, \
		C_SexUnkn,C_AllResTypes,\
		C_Age_0_4,C_Age_5_14,C_Age_15_24,C_Age_25_34,C_Age_35_44,C_Age_45_54, \
		C_Age_55_64,C_Age_65_74,C_Age_75_84,C_Age_85plus,C_Age_Unkn,C_AgeRange, \
		C_AgeMedian,C_RaceWhite,C_RaceBlack,C_RaceOther,C_RaceUnknown,C_HispanicYES, \
		C_HispanicNO,C_HispanicUnk,C_EDYes_Res,C_EDYes_NonRes,C_HospYes_Res, \
		C_HospYes_NonRes,C_NonResDeaths,C_FLResDeaths,CasesAll,C_Men,C_Women, \
		C_FLRes,C_NotFLRes,C_FLResOut,T_NegRes,T_NegNotFLRes,T_total,T_negative, \
		T_positive,Deaths,"New Cases","New Negative cases","New Total Tested Today", \
		"New Percent Positivity",MedianAge)  \
		VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,? \
		,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(eDate, \
		input['OBJECTID_12_13'],input['DEPCODE'],input['COUNTYNAME'], \
		input['County_1'],input['State'], input['T_Total_Res'], \
		input['C_Female'],input['C_Male'],input['C_SexUnkn'],input['C_AllResTypes'], \
		input['C_Age_0_4'],input['C_Age_5_14'],input['C_Age_15_24'],input['C_Age_25_34'],
		input['C_Age_35_44'],input['C_Age_45_54'],input['C_Age_55_64'],input['C_Age_65_74'], \
		input['C_Age_75_84'],input['C_Age_85plus'],input['C_Age_Unkn'],input['C_AgeRange'], \
		input['C_AgeMedian'],input['C_RaceWhite'],input['C_RaceBlack'],input['C_RaceOther'], \
		input['C_RaceUnknown'],input['C_HispanicYES'],input['C_HispanicNO'], \
		input['C_HispanicUnk'],input['C_EDYes_Res'],input['C_EDYes_NonRes'], \
		input['C_HospYes_Res'],input['C_HospYes_NonRes'],input['C_NonResDeaths'], \
		input['C_FLResDeaths'],input['CasesAll'],input['C_Men'],input['C_Women'], \
		input['C_FLRes'],input['C_NotFLRes'],input['C_FLResOut'],input['T_NegRes'], \
		input['T_NegNotFLRes'],input['T_total'],input['T_negative'],input['T_positive'], \
		input['Deaths'],input['NewPos'],input['NewNeg'],input['NewTested'],  \
		input['NewPercPos'], input['MedianAge']))

		conn.commit()

	conn.close()

	print("Building Vaccine DB")
	fetchVaccine()

	
if __name__ == "__main__":
	updateCounty()
