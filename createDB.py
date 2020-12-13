import sqlite3 as sql

conn = sql.connect('covid_data.db')

conn.execute('CREATE TABLE Patients(ObjectID INT,\
County TEXT,\
Age INT,\
Age_group TEXT,\
Gender TEXT,\
Jurisdiction TEXT,\
Travel_related TEXT,\
Origin TEXT,\
EDVisit TEXT,\
Hospitalized TEXT,\
Died TEXT,\
CaseStatus TEXT,\
Contact TEXT,\
CaseDate INT,\
EventDate INT,\
ChartDate INT,\
PRIMARY KEY (ObjectID))')

conn.execute('CREATE TABLE Zips(ZipCode TEXT,\
County TEXT,\
Places TEXT,\
PlacesReport TEXT,\
NumberCases,\
PRIMARY KEY(ZipCode))')

conn.execute('CREATE TABLE Totals (DateEpoch INT,\
Negative INT,\
Positive INT,\
Total INT,\
PRIMARY KEY (DateEpoch))')

conn.close()

conn = sql.connect('quickAccess.db')
conn.execute('CREATE TABLE Quick(Total INT,\
Resident INT, \
NonResident INT, \
ResHosp INT, \
NonResHosp INT, \
ResDeath INT, \
NonResDeath INT, \
PRIMARY KEY(TOTAL));  

