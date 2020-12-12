import sqlite3 as sql

conn = sql.connect('covid_data.db')

#conn.execute('CREATE TABLE Line

#conn.execute('CREATE TABLE County

#conn.execute('CREATE TABLE Zip

conn.execute('CREATE TABLE Totals (DateEpoch INT,\
Negative INT,\
Positive INT,\
Total INT,\
PRIMARY KEY (DateEpoch))')

conn.close()
