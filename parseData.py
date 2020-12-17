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

	#Return Results
	return output

#Get previous days results
def getPrevDayCounty(name):

	#Connect to Database
	conn = sql.connect("County.db")
	cur = conn.cursor()

	#Pull last 30 days of resident results
	cur.execute("SELECT DateStamp, C_Female, C_Male, C_SexUnkn, C_Women, C_Men,\
	C_RaceWhite, C_RaceBlack, C_RaceOther, C_RaceUnknown, \
	C_HispanicYes, C_HispanicNo, C_HispanicUnk, C_EDYes_Res, \
	C_EDYes_NonRes, C_HospYes_Res, C_HospYes_NonRes, \
	T_negative, T_positive, T_NegRes, T_NegNotFLRes,C_FLRes,C_NotFLRes \
	FROM County WHERE County = ? \
	GROUP BY DateStamp Order BY DateStamp DESC LIMIT 2",(name,))

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
		 AND Jurisdiction != "Non-FL resident" AND County = ? \
		 GROUP BY Age ORDER BY Age ASC', (timestamp,name))

	rows = cur.fetchall()

	subtotal = 0
	entry = 0

	if not rows:
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
	else:
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
	print (name)
	#Grab ALL age Information
	cur.execute('SELECT Age,COUNT(Age) FROM Patients WHERE CaseDate = ? \
		 AND Jurisdiction = "Non-FL resident" AND County = ? \
		 GROUP BY Age ORDER BY Age ASC', (timestamp,name))

	rows = cur.fetchall()

	print(rows)
	subtotal = 0
	entry = 0

	if not rows:
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
	else:
		#Sum up each age chunk and add to output
		for i in range(0,130):
			print(i)
			if i == (rows[entry][0]):
				subtotal += rows[int(entry)][1]
				if entry < len(rows)-1:
					entry += 1
			else:
				subtotal=subtotal
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
		 AND Jurisdiction != "Non-FL resident" AND Gender = "Male" \
		 AND County = ?',(timestamp,name))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Female Gender Positive Tests For Res
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate = ? \
		 AND Jurisdiction != "Non-FL resident" AND Gender = "Female" \
		 AND County = ?',(timestamp,name))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Unknown Gender Positive Tests For Res
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate = ? \
		 AND Jurisdiction != "Non-FL resident" AND Gender = "Unknown" \
		 AND County = ?',(timestamp,name))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Male Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate = ? \
		 AND Jurisdiction = "Non-FL resident" AND Gender = "Male" \
		 AND County = ?',(timestamp,name))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Female Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate = ? \
		 AND Jurisdiction = "Non-FL resident" AND Gender = "Female" \
		 AND County = ?',(timestamp,name))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Unknown Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate = ? \
		 AND Jurisdiction = "Non-FL resident" AND Gender = "Unknown" \
		 AND County = ?',(timestamp,name))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	conn.close()

	#Get Population information
	conn = sql.connect("pop_data.db")
	cur = conn.cursor()

	print (name)
	cur.execute('SELECT County,Population FROM Pop WHERE County = ?', (name,))
	rows = cur.fetchall()
	print(rows)
	output.append(rows[0][0])
	output.append(rows[0][1])

	#Return Results
	return output

#Get previous days results
def getPrevRangeCounty(name,num):

	#Connect to Database
	conn = sql.connect("County.db")
	cur = conn.cursor()

	#Pull last 30 days of resident results
	cur.execute("SELECT DateStamp, C_Female, C_Male, C_SexUnkn, C_Women, C_Men,\
	C_RaceWhite, C_RaceBlack, C_RaceOther, C_RaceUnknown, \
	C_HispanicYes, C_HispanicNo, C_HispanicUnk, C_EDYes_Res, \
	C_EDYes_NonRes, C_HospYes_Res, C_HospYes_NonRes, \
	T_negative, T_positive, T_NegRes, T_NegNotFLRes,C_FLRes,C_NotFLRes \
	FROM County WHERE County = ? \
	GROUP BY DateStamp Order BY DateStamp DESC LIMIT ?",(name,int(num)+1))

	rows = cur.fetchall()
	#Flip order of results
	rows.reverse()

	output = []

	output.append(time.strftime("%m/%d/%Y",time.gmtime(int(rows[0][0])/1000)))

	#
	for i in range(1,len(rows[0])):
		output.append((int(rows[int(num)][i]) - int(rows[0][i])))

	conn.close()

	timeStart = rows[0][0]
	timeEnd = rows[int(num)][0]

	#Fetch Resident Age Groups totals for the day
	#Connect to Patient DB
	conn = sql.connect("covid_data.db")
	cur = conn.cursor()

	#Get lastest date
	cur.execute('SELECT MAX(ChartDate) FROM Patients')
	timestamp = (cur.fetchall())[0][0]

	#Grab ALL age Information
	cur.execute('SELECT Age,COUNT(Age) FROM Patients WHERE CaseDate <= ? \
		AND CaseDate > ?\
		AND Jurisdiction != "Non-FL resident" AND County = ? \
		GROUP BY Age ORDER BY Age ASC', (timeEnd,timeStart,name))

	rows = cur.fetchall()

	subtotal = 0
	entry = 0

	if not rows:
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
	else:
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
	cur.execute('SELECT Age,COUNT(Age) FROM Patients WHERE CaseDate <= ? \
		AND CaseDate > ? \
		AND Jurisdiction = "Non-FL resident" AND County = ? \
		GROUP BY Age ORDER BY Age ASC', (timeEnd,timeStart,name))

	rows = cur.fetchall()

	subtotal = 0
	entry = 0

	if not rows:
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
	else:
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
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate <= ? \
		 AND Jurisdiction != "Non-FL resident" AND Gender = "Male" \
		 AND CaseDate > ? AND County = ?',(timeEnd,timeStart,name))

	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Female Gender Positive Tests For Res
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate <= ? \
		 AND Jurisdiction != "Non-FL resident" AND Gender = "Female" \
		 AND CaseDate > ? AND County = ?',(timeEnd,timeStart,name))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Unknown Gender Positive Tests For Res
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate <= ? \
		 AND Jurisdiction != "Non-FL resident" AND Gender = "Unknown" \
		 AND CaseDate > ? AND County = ?',(timeEnd,timeStart,name))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Male Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate <= ? \
		 AND Jurisdiction = "Non-FL resident" AND Gender = "Male" \
		 AND CaseDate > ? AND County = ?',(timeEnd,timeStart,name))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Female Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate <= ? \
		 AND Jurisdiction = "Non-FL resident" AND Gender = "Female" \
		 AND CaseDate > ? AND County = ?',(timeEnd,timeStart,name))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Unknown Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate = ? \
		 AND Jurisdiction = "Non-FL resident" AND Gender = "Unknown" \
		 AND CaseDate > ? AND County = ?',(timeEnd,timeStart,name))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	conn.close()

	#Get Population information
	conn = sql.connect("pop_data.db")
	cur = conn.cursor()

	print (name)
	cur.execute('SELECT County,Population FROM Pop WHERE County = ?', (name,))
	rows = cur.fetchall()
	print(rows)
	output.append(rows[0][0])
	output.append(rows[0][1])

	#Return Results
	return output

#Get previous days results
def getPrevRangeState(num):

	#Connect to Database
	conn = sql.connect("County.db")
	cur = conn.cursor()

	value = int(num)+1
	#Pull last num days of resident results
	cur.execute("SELECT DateStamp, C_Female, C_Male, C_SexUnkn, C_Women, C_Men,\
	C_RaceWhite, C_RaceBlack, C_RaceOther, C_RaceUnknown, \
	C_HispanicYes, C_HispanicNo, C_HispanicUnk, C_EDYes_Res, \
	C_EDYes_NonRes, C_HospYes_Res, C_HospYes_NonRes, \
	T_negative, T_positive, T_NegRes, T_NegNotFLRes,C_FLRes,C_NotFLRes \
	FROM County WHERE County = 'State' \
	GROUP BY DateStamp Order BY DateStamp DESC LIMIT ?",(value,))

	rows = cur.fetchall()
	#Flip order of results
	rows.reverse()

	output = []

	output.append(time.strftime("%m/%d/%Y",time.gmtime(int(rows[0][0])/1000)))

	#
	for i in range(1,len(rows[0])):
		output.append((int(rows[int(num)][i]) - int(rows[0][i])))

	conn.close()

	timeStart = rows[0][0]
	timeEnd = rows[int(num)][0]

	#Fetch Resident Age Groups totals for the day
	#Connect to Patient DB
	conn = sql.connect("covid_data.db")
	cur = conn.cursor()

	#Get lastest date
	cur.execute('SELECT MAX(ChartDate) FROM Patients')
	timestamp = (cur.fetchall())[0][0]

	#Grab ALL age Information
	cur.execute('SELECT Age,COUNT(Age) FROM Patients WHERE CaseDate <= ? \
		AND CaseDate > ?\
		AND Jurisdiction != "Non-FL resident" \
		GROUP BY Age ORDER BY Age ASC', (timeEnd,timeStart))

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
	cur.execute('SELECT Age,COUNT(Age) FROM Patients WHERE CaseDate <= ? \
		AND CaseDate > ? \
		AND Jurisdiction = "Non-FL resident"\
		GROUP BY Age ORDER BY Age ASC', (timeEnd,timeStart))

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
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate <= ? \
		 AND Jurisdiction != "Non-FL resident" AND Gender = "Male" \
		 AND CaseDate > ?',(timeEnd,timeStart))

	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Female Gender Positive Tests For Res
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate <= ? \
		 AND Jurisdiction != "Non-FL resident" AND Gender = "Female" \
		 AND CaseDate > ?',(timeEnd,timeStart))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Unknown Gender Positive Tests For Res
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate <= ? \
		 AND Jurisdiction != "Non-FL resident" AND Gender = "Unknown" \
		 AND CaseDate > ?',(timeEnd,timeStart))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Male Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate <= ? \
		 AND Jurisdiction = "Non-FL resident" AND Gender = "Male" \
		 AND CaseDate > ?',(timeEnd,timeStart))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Female Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate <= ? \
		 AND Jurisdiction = "Non-FL resident" AND Gender = "Female" \
		 AND CaseDate > ?',(timeEnd,timeStart))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Unknown Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients WHERE CaseDate = ? \
		 AND Jurisdiction = "Non-FL resident" AND Gender = "Unknown" \
		 AND CaseDate > ?',(timeEnd,timeStart))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	conn.close()

	#Get Population information
	conn = sql.connect("pop_data.db")
	cur = conn.cursor()

	cur.execute('SELECT County,Population FROM Pop WHERE County = "State"')
	rows = cur.fetchall()
	print(rows)
	output.append(rows[0][0])
	output.append(rows[0][1])

	#Return Results
	return output

#Get previous days results
def getAllCounty(name):

	#Connect to Database
	conn = sql.connect("County.db")
	cur = conn.cursor()

	#Pull last 30 days of resident results
	cur.execute("SELECT DateStamp, C_Female, C_Male, C_SexUnkn, C_Women, C_Men,\
	C_RaceWhite, C_RaceBlack, C_RaceOther, C_RaceUnknown, \
	C_HispanicYes, C_HispanicNo, C_HispanicUnk, C_EDYes_Res, \
	C_EDYes_NonRes, C_HospYes_Res, C_HospYes_NonRes, \
	T_negative, T_positive, T_NegRes, T_NegNotFLRes,C_FLRes,C_NotFLRes \
	FROM County WHERE County = ? \
	GROUP BY DateStamp Order BY DateStamp DESC LIMIT 1",(name,))

	rows = cur.fetchall()
	#Flip order of results
	rows.reverse()

	output = []

	output.append(time.strftime("%m/%d/%Y",time.gmtime(int(rows[0][0])/1000)))

	#
	for i in range(1,len(rows[0])):
		output.append(int(rows[0][i]))

	conn.close()

	#Fetch Resident Age Groups totals for the day
	#Connect to Patient DB
	conn = sql.connect("covid_data.db")
	cur = conn.cursor()

	#Grab ALL age Information
	cur.execute('SELECT Age,COUNT(Age) FROM Patients \
		WHERE Jurisdiction != "Non-FL resident" AND County = ? \
		GROUP BY Age ORDER BY Age ASC', (name,))

	rows = cur.fetchall()

	subtotal = 0
	entry = 0

	if not rows:
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
	else:
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
	cur.execute('SELECT Age,COUNT(Age) FROM Patients \
		WHERE Jurisdiction = "Non-FL resident" AND County = ? \
		GROUP BY Age ORDER BY Age ASC', (name,))

	rows = cur.fetchall()

	subtotal = 0
	entry = 0

	if not rows:
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
	else:
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
	cur.execute('SELECT COUNT(*) FROM Patients \
		 WHERE Jurisdiction != "Non-FL resident" AND Gender = "Male" \
		 AND County = ?',(name,))

	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Female Gender Positive Tests For Res
	cur.execute('SELECT COUNT(*) FROM Patients \
		 WHERE Jurisdiction != "Non-FL resident" AND Gender = "Female" \
		 AND County = ?',(name,))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Unknown Gender Positive Tests For Res
	cur.execute('SELECT COUNT(*) FROM Patients \
		 WHERE Jurisdiction != "Non-FL resident" AND Gender = "Unknown" \
		 AND County = ?',(name,))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Male Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients \
		 WHERE Jurisdiction = "Non-FL resident" AND Gender = "Male" \
		 AND County = ?',(name,))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Female Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients \
		 WHERE Jurisdiction = "Non-FL resident" AND Gender = "Female" \
		 AND County = ?',(name,))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Unknown Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients \
		 WHERE Jurisdiction = "Non-FL resident" AND Gender = "Unknown" \
		 AND County = ?',(name,))
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	conn.close()

	#Get Population information
	conn = sql.connect("pop_data.db")
	cur = conn.cursor()

	print (name)
	cur.execute('SELECT County,Population FROM Pop WHERE County = ?', (name,))
	rows = cur.fetchall()
	print(rows)
	output.append(rows[0][0])
	output.append(rows[0][1])

	#Return Results
	return output

#Get all results
def getAllState():

	#You're in good hands

	#Connect to Database
	conn = sql.connect("County.db")
	cur = conn.cursor()

	#Pull last 30 days of resident results
	cur.execute("SELECT DateStamp, C_Female, C_Male, C_SexUnkn, C_Women, C_Men,\
	C_RaceWhite, C_RaceBlack, C_RaceOther, C_RaceUnknown, \
	C_HispanicYes, C_HispanicNo, C_HispanicUnk, C_EDYes_Res, \
	C_EDYes_NonRes, C_HospYes_Res, C_HospYes_NonRes, \
	T_negative, T_positive, T_NegRes, T_NegNotFLRes,C_FLRes,C_NotFLRes \
	FROM County WHERE County = 'State' \
	GROUP BY DateStamp Order BY DateStamp DESC LIMIT 1")

	rows = cur.fetchall()
	#Flip order of results
	rows.reverse()

	output = []

	output.append(time.strftime("%m/%d/%Y",time.gmtime(int(rows[0][0])/1000)))

	#
	for i in range(1,len(rows[0])):
		output.append(int(rows[0][i]))

	conn.close()

	#Fetch Resident Age Groups totals for the day
	#Connect to Patient DB
	conn = sql.connect("covid_data.db")
	cur = conn.cursor()

	#Grab ALL age Information
	cur.execute('SELECT Age,COUNT(Age) FROM Patients \
		WHERE Jurisdiction != "Non-FL resident" \
		GROUP BY Age ORDER BY Age ASC')

	rows = cur.fetchall()

	subtotal = 0
	entry = 0

	if not rows:
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
	else:
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
	cur.execute('SELECT Age,COUNT(Age) FROM Patients \
		WHERE Jurisdiction = "Non-FL resident" \
		GROUP BY Age ORDER BY Age ASC')

	rows = cur.fetchall()

	subtotal = 0
	entry = 0

	if not rows:
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
		output.append(0)
	else:
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
	cur.execute('SELECT COUNT(*) FROM Patients \
		 WHERE Jurisdiction != "Non-FL resident" AND Gender = "Male" ')

	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Female Gender Positive Tests For Res
	cur.execute('SELECT COUNT(*) FROM Patients \
		 WHERE Jurisdiction != "Non-FL resident" AND Gender = "Female" ')
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Unknown Gender Positive Tests For Res
	cur.execute('SELECT COUNT(*) FROM Patients \
		 WHERE Jurisdiction != "Non-FL resident" AND Gender = "Unknown"')
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Male Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients \
		 WHERE Jurisdiction = "Non-FL resident" AND Gender = "Male" ')
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Female Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients \
		 WHERE Jurisdiction = "Non-FL resident" AND Gender = "Female"')
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	#Fetch Unknown Gender Positive Tests For NonRes
	cur.execute('SELECT COUNT(*) FROM Patients \
		 WHERE Jurisdiction = "Non-FL resident" AND Gender = "Unknown"')
	rows = cur.fetchall()
	if not rows:
		output.append(0)
	else:
		output.append(rows[0][0])

	conn.close()

	#Get Population information
	conn = sql.connect("pop_data.db")
	cur = conn.cursor()

	cur.execute('SELECT County,Population FROM Pop WHERE County = "State"')
	rows = cur.fetchall()
	output.append(rows[0][0])
	output.append(rows[0][1])

	#Return Results
	return output


if __name__ == "__main__":
	getPrevDay()



