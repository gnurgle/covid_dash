import sqlite3 as sql
import time

#Grab the last 30 days of positive resident results
def getPos30():

	#Connect to Database
	conn = sql.connect("covid_data.db")
	cur = conn.cursor()

	#Pull last 30 days of resident results
	cur.execute("SELECT CaseDate, COUNT(*) FROM Patients WHERE "\
	+ "Jurisdiction != 'Non-FL resident' GROUP BY CaseDate " \
	+ "ORDER BY CaseDate DESC LIMIT 30")

	rows = cur.fetchall()
	#Flip order of results
	rows.reverse()
	output = []

	#Grab last 30 days of nonresident results
	cur.execute("SELECT CaseDate, COUNT(*) FROM Patients WHERE "\
	+ "Jurisdiction = 'Non-FL resident' GROUP BY CaseDate " \
	+ "ORDER BY CaseDate DESC LIMIT 30")

	rows2 = cur.fetchall()
	rows2.reverse()

	#Convert epoch time to a date
	for i in range(0,len(rows)):
		value = time.strftime("%m/%d/%Y",time.gmtime((rows[i][0]/1000)))
		output.append((value, rows[i][1], rows2[i][1]))

	#Change results of rows to fit chart
	output = list(zip(*output))
	#Return Results
	return output

#Grab the last 30 days of positive resident results
def getDeaths30():

	#Connect to Database
	conn = sql.connect("covid_data.db")
	cur = conn.cursor()

	#Pull last 30 days of resident results
	cur.execute("SELECT CaseDate, COUNT(*) FROM Patients WHERE "\
	+ "Jurisdiction != 'Non-FL resident' AND Died != 'NA'"\
	+ "GROUP BY CaseDate " \
	+ "ORDER BY CaseDate DESC LIMIT 30")

	rows = cur.fetchall()
	#Flip order of results
	rows.reverse()
	output = []

	#Grab last 30 days of nonresident results
	cur.execute("SELECT CaseDate, COUNT(*) FROM Patients WHERE "\
	+ "Jurisdiction = 'Non-FL resident' AND Died != 'NA'"\
	+ "GROUP BY CaseDate " \
	+ "ORDER BY CaseDate DESC LIMIT 30")

	rows2 = cur.fetchall()
	rows2.reverse()

	#Convert epoch time to a date
	for i in range(0,len(rows)):
		value = time.strftime("%m/%d/%Y",time.gmtime(int(rows[i][0])/1000))
		output.append((value, rows[i][1], rows2[i][1]))

	#Change results of rows to fit chart
	output = list(zip(*output))
	#Return Results
	return output

#Get previous days results
def getPrevDay():

	#Connect to Database
	conn = sql.connect("County.db")
	cur = conn.cursor()

	#Pull last 30 days of resident results
	cur.execute("SELECT DateStamp, C_Female, C_Male, C_SexUnkn, C_Women, C_Men,"\
	+ "C_RaceWhite, C_RaceBlack, C_RaceOther, C_RaceUnknown, "\
	+ "C_HispanicYes, C_HispanicNo, C_HispanicUnk, C_EDYes_Res, "\
	+ "C_EDYes_NonRes, C_HospYes_Res, C_HospYes_NonRes, "\
	+ "T_negative, T_positive, T_NegRes, T_NegNotFLRes,C_FLRes,C_NotFLRes "\
	+ "FROM County WHERE County = 'State' "\
	+ "GROUP BY DateStamp Order BY DateStamp DESC LIMIT 2")

	rows = cur.fetchall()
	#Flip order of results
	rows.reverse()

	output = []

	output.append(time.strftime("%m/%d/%Y",time.gmtime(int(rows[0][0])/1000)))

	#
	for i in range(1,len(rows[0])):
		output.append((int(rows[1][i]) - int(rows[0][i])))

	conn.close()

	#Fetch Resident Age Groups totals for the day
	#Connect to Patient DB
	conn = sql.connect("covid_data.db")
	cur = conn.cursor()

	#Get lastest date
	cur.execute('SELECT MAX(ChartDate) FROM Patients')
	timestamp = (cur.fetchall())[0][0]

	#Grab ALL age Information
	cur.execute('SELECT Age,COUNT(Age) FROM Patients WHERE CaseDate = ? \
		 AND Jurisdiction != "Non-FL resident" GROUP BY Age ORDER BY Age ASC', (timestamp,))

	rows = cur.fetchall()

	subtotal = 0
	entry = 0
	#Sum up each age chunk and add to output
	for i in range(0,130):
		if i == rows[entry][0]:
			subtotal += rows[entry][1]
			if entry < len(rows)-1:
				entry += 1
		if i % 10 == 4 and i<85:
			output.append(subtotal)
			subtotal = 0
	#Add 85+ group
	output.append(subtotal)

	#Fetch Non-Resident Age Groups totals for the day

	#Grab ALL age Information
	cur.execute('SELECT Age,COUNT(Age) FROM Patients WHERE CaseDate = ? \
		 AND Jurisdiction = "Non-FL resident" GROUP BY Age ORDER BY Age ASC', (timestamp,))

	rows = cur.fetchall()

	subtotal = 0
	entry = 0

	#Sum up each age chunk and add to output
	for i in range(0,130):
		if i == rows[entry][0]:
			subtotal += rows[entry][1]
			if entry < len(rows)-1:
				entry += 1
		if i % 10 == 4 and i<85:
			output.append(subtotal)
			subtotal = 0
	#Add 85+ group
	output.append(subtotal)

	#The reason that the queries are split up vs running a group
	#Is due to the potential for an Unknown or a specific gender to not
	#be represented. 

	#Fetch Male Gender Positive Tests For Res
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate = ? \
		 AND Jurisdiction != "Non-FL resident" AND Gender = "Male"',(timestamp,))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Female Gender Positive Tests For Res
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate = ? \
		 AND Jurisdiction != "Non-FL resident" AND Gender = "Female"',(timestamp,))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Unknown Gender Positive Tests For Res
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate = ? \
		 AND Jurisdiction != "Non-FL resident" AND Gender = "Unknown"',(timestamp,))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Male Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate = ? \
		 AND Jurisdiction = "Non-FL resident" AND Gender = "Male"',(timestamp,))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Female Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate = ? \
		 AND Jurisdiction = "Non-FL resident" AND Gender = "Female"',(timestamp,))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Unknown Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate = ? \
		 AND Jurisdiction = "Non-FL resident" AND Gender = "Unknown"',(timestamp,))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	conn.close()

	#Connect to Database
	conn = sql.connect("County.db")
	cur = conn.cursor()

	#Return Results
	return output

#Get previous days results
def getPrevDayCounty(name):

	#Connect to Database
	conn = sql.connect("County.db")
	cur = conn.cursor()

	#Pull last 30 days of resident results
	cur.execute('SELECT DateStamp, C_Female, C_Male, C_SexUnkn, C_Women, C_Men, C_Age_0_4, \
	 C_Age_5_14, C_Age_15_24, C_Age_25_34, C_Age_35_44,  \
	C_Age_45_54, C_Age_55_64, C_Age_65_74, C_Age_75_84, C_Age_85plus,  \
	C_Age_Unkn, C_RaceWhite, C_RaceBlack, C_RaceOther, C_RaceUnknown,  \
	C_HispanicYes, C_HispanicNo, C_HispanicUnk, C_EDYes_Res,  \
	C_EDYes_NonRes, C_HospYes_Res, C_HospYes_NonRes,  \
	T_negative, T_positive, T_NegRes, T_NegNotFLRes  \
	FROM County WHERE County = ? \
	GROUP BY DateStamp Order BY DateStamp DESC LIMIT 2 VALUES(?)',(name,))

	rows = cur.fetchall()
	#Flip order of results
	rows.reverse()

	output = []

	output.append(time.strftime("%m/%d/%Y",time.gmtime(int(rows[0][0])/1000)))

	#
	for i in range(1,len(rows[0])):
		if i == 17:
			print (rows[1][i])
			print (rows[1][i])
		output.append((int(rows[1][i]) - int(rows[0][i])))

	#Return Results
	return output


if __name__ == "__main__":
	getPrevDay()



