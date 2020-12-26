import requests
import io
import pdfminer
from pdfminer.high_level import extract_text
import datetime
import sqlite3 as sql
import decimal

#Get Vaccine information
def fetchVaccine():

	#Set URL
	url = "http://ww11.doh.state.fl.us/comm/_partners/" \
	+ "covid19_report_archive/vaccine/vaccine_report_latest.pdf"

	#Fetch PDF and set to byte stream in memory
	response = requests.get(url)
	pdfObj = io.BytesIO(response.content)

	#extract text contents and set newline to list entry
	output = extract_text(pdfObj)
	outList = output.splitlines()

	#Display line contents of outList
	#Left in for debugging if needed
	#lineNum = 0
	#for entry in outList:
	#	print(str(lineNum) + ": " + str(entry))
	#	lineNum += 1



	#=======================================
	#This section relates to the first page table
	#=======================================

	raceCol1 = outList[100:110:2]
	raceCol2 = outList[136:146:2]
	ageCol1 = outList[112:128:2]
	ageCol2 = outList[148:164:2]
	genderCol1 = outList[130:136:2]
	genderCol2 = outList[166:172:2]
	totalCol = []
	totalCol.append(outList[98])
	totalCol.append(outList[136])
	#temp assigning overdue to series complete until finalized
	totalCol.append(outList[136])

	#Strip commas out
	for i in range(0,len(raceCol1)):
		raceCol1[i] = raceCol1[i].replace(',','')
	for i in range(0,len(ageCol1)):
		ageCol1[i] = ageCol1[i].replace(',','')
	for i in range(0,len(genderCol1)):
		genderCol1[i] = genderCol1[i].replace(',','')
	for i in range(0,len(raceCol2)):
		raceCol2[i] = raceCol2[i].replace(',','')
	for i in range(0,len(ageCol2)):
		ageCol2[i] = ageCol2[i].replace(',','')
	for i in range(0,len(genderCol2)):
		genderCol2[i] = genderCol2[i].replace(',','')
	for i in range(0,len(totalCol)):
		totalCol[i] = totalCol[i].replace(',','')

	#Combine columns into single

	tempRace = []
	tempAge = []
	tempGender = []

	tempRace.append(raceCol1)
	tempRace.append(raceCol2)
	tempAge.append(ageCol1)
	tempAge.append(ageCol2)
	tempGender.append(genderCol1)
	tempGender.append(genderCol2)

	#Change formatting to fit table better
	tempRace = list(zip(*tempRace))
	tempAge = list(zip(*tempAge))
	tempGender = list(zip(*tempGender))

	#Get timestamp
	timeStamp = int(datetime.datetime.now().timestamp())
	
	#Add all numbers to final output
	bDownList = []
	bDownList.append(timeStamp)
	for entry in tempRace:
		for val in entry:
			bDownList.append(int(val))
	for entry in tempAge:
		for val in entry:
			bDownList.append(int(val))
	for entry in tempGender:
		for val in entry:
			bDownList.append(int(val))
	for entry in totalCol:
		bDownList.append(int(entry))

	#===============================
	#End second table
	#===============================

	#=======================================
	#This section relates to the second page table
	#=======================================

	vacCol0 = outList[293:362]
	vacCol1 = outList[364:433]
	vacCol2 = outList[579:648]
	vacCol3 = outList[437:506]
	vacCol4 = outList[508:577]
	vacCol5 = outList[723:792]
	vacCol6 = outList[652:721]

	#Strip commas out
	for i in range(0,69):
		vacCol1[i] = vacCol1[i].replace(',','')
	for i in range(0,69):
		vacCol2[i] = vacCol2[i].replace(',','')
	for i in range(0,69):
		vacCol3[i] = vacCol3[i].replace(',','')
	for i in range(0,69):
		vacCol4[i] = vacCol4[i].replace(',','')
	for i in range(0,69):
		vacCol5[i] = vacCol5[i].replace(',','')
	for i in range(0,69):
		vacCol6[i] = vacCol6[i].replace(',','')


	countyComb = []
	#Combine all columns into single list
	for i in range(0,68):
		countyComb.append((vacCol0[i],vacCol1[i],vacCol2[i],\
			vacCol3[i],vacCol4[i],vacCol5[i],vacCol6[i]))

	#===============================
	#End second table
	#===============================

	#=======================================
	#This section relates to the Database intergration
	#=======================================

	#Connect to DB
	conn = sql.connect("vaccine_db.db")
	cur = conn.cursor()

	#Insert new Breakdown
	cur.execute ("INSERT INTO Breakdown \
		VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",\
		(bDownList[:]))

	#Remove old breakdown
	cur.execute ("DELETE FROM Breakdown WHERE Timestamp != ?",(timeStamp,))

	#Commit Changes
	conn.commit()

	#Run for each county 
	for entry in countyComb:

		#Get population as int
		cur.execute("SELECT Pop FROM CountyVac WHERE County = ?",(entry[0],))
		popul = int((cur.fetchall())[0][0])

		#Calculate new percentage using decimal for higher accuracy
		if popul != 0:
			newPerc = decimal.Decimal(entry[6])/decimal.Decimal(popul)
			newPerc = newPerc*100
			newPerc = round(newPerc,2)
		else:
			newPerc = 0.00

		#Remove Old Entry
		cur.execute("DELETE FROM CountyVac WHERE County = ?",(entry[0],))
		conn.commit()

		#Add new Entry
		cur.execute("INSERT INTO CountyVac VALUES(?,?,?,?,?,?,?,?,?)",\
			(entry[0],entry[1],entry[2],entry[3],entry[4],entry[5],entry[6],popul,str(newPerc)))
		conn.commit()

	conn.close()
	#===============================
	#End Database
	#===============================
	

if __name__=="__main__":
	fetchVaccine()
