import database as db
import numpy as np
import pandas as pd
import datetime as dt
import time
from binance.client import Client
from keys import key, secret

client = Client(key, secret)
earliest = '1 Jan, 2017'

pairs = [
	'BTCUSDT',
	'BNBUSDT',
	'BNBBTC',
	'ETHUSDT',
	'ETHBTC',
	'LTCUSDT',
	'LTCBTC',
	'BCHABCUSDT',
	'BCHABCBTC',
	'XRPUSDT',
	'XRPBTC',
	'ADABTC',
	'EOSUSDT',
	'EOSBTC',
	'NANOBTC',
	'LINKBTC'
]

def cleanCandles(candles):
	for candle in candles:
		candle[11] = str(dt.datetime.utcfromtimestamp(float(candle[6])/1000.0))
		floaters = [1,2,3,4,5,7,9,10]
		for floater in floaters:
			candle[floater] = float(candle[floater])

def scrape(pairs):
	conn, c = db.init('tradingPairs.db')

	for pair in pairs:
		print('Scrape: Updating ' + pair + '...')
		fromDate = ''

		last = db.getLastDate(c, pair)
		if last:
			fromDate = last[0][0]
		else:
			fromDate = earliest

		candles = client.get_historical_klines(pair, Client.KLINE_INTERVAL_1MINUTE, fromDate)
		cleanCandles(candles)
		for candle in candles:
			db.dataEntry(c, conn, pair, candle)

	db.close(c, conn)

if __name__ == '__main__':
	while True:
		print('Scraping, DO NOT STOP')
		scrape(pairs)
		print('You can stop this now...')
		time.sleep(270)
		print('You have 30 seconds left to stop this...')
		time.sleep(30)