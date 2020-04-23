import sqlite3, time
import datetime as dt

def init(database):
	conn = sqlite3.connect('tradingPairs.db')
	c = conn.cursor()
	return conn, c

def close(c, conn):
	c.close()
	conn.close()

def createTables(pairs):
	for pair in pairs:
		c.execute('CREATE TABLE IF NOT EXISTS '+pair+'(openTime REAL, open REAL, high REAL, low REAL, close REAL, volume REAL, closeTime REAL, qav REAL, trades REAL, tbbav REAL, tbqav REAL, date TEXT)')

def dataEntry(c, conn, pair, candle):
	c.execute("INSERT INTO "+pair+"(openTime, open, high, low, close, volume, closeTime, qav, trades, tbbav, tbqav, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
			(candle[0], candle[1], candle[2], candle[3], candle[4], candle[5], candle[6], candle[7], candle[8], candle[9], candle[10], candle[11]))
	conn.commit()

def getLastDate(c, pair):
	c.execute('SELECT date FROM '+pair+' ORDER BY closeTime DESC LIMIT 1;')
	return c.fetchall()

def getAll(c, pair, resolution):
	c.execute('SELECT date, close FROM '+pair+' WHERE rowid % '+resolution+' = 0')
	return c.fetchall()

def getSince(c, pair, resolution, span):
	stamp = str((time.time() - span*60)*1000)
	print(stamp)
	c.execute('SELECT date, close FROM '+pair+' WHERE closeTime >= '+stamp+' AND rowid % '+resolution+' = 0')
	return c.fetchall()