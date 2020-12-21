import sqlite3 as sql
import 


def drawMap():

	#Connect to DB
	conn = sql.connect("County.db")
	cur = conn.cursor()


if __name__ == "__main__":
	drawMap()
