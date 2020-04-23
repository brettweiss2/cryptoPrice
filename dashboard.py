import dash, sqlite3
import database as db
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd

app = dash.Dash()

df = pd.read_csv('data/LINKBTC.csv', delimiter = ',')

app.layout = html.Div(children=[
	html.H1('Binance Market Data'),

	dcc.Dropdown(id='tradingPair',
		options=[
			{'label': 'BTC/USDT', 'value': 'BTCUSDT'},
			{'label': 'ETH/USDT', 'value': 'ETHUSDT'},
			{'label': 'ETH/BTC', 'value': 'ETHBTC'},
			{'label': 'LTC/USDT', 'value': 'LTCUSDT'},
			{'label': 'LTC/BTC', 'value': 'LTCBTC'},
			{'label': 'BCH/USDT', 'value': 'BCHABCUSDT'},
			{'label': 'BCH/BTC', 'value': 'BCHABCBTC'},
			{'label': 'XRP/USDT', 'value': 'XRPUSDT'},
			{'label': 'XRP/BTC', 'value': 'XRPBTC'},
			{'label': 'EOS/USDT', 'value': 'EOSUSDT'},
			{'label': 'EOS/BTC', 'value': 'EOSBTC'},
			{'label': 'ADA/BTC', 'value': 'ADABTC'},
			{'label': 'NANO/BTC', 'value': 'NANOBTC'},
			{'label': 'LINK/BTC', 'value': 'LINKBTC'}
		],
		value='LINKBTC'),

	dcc.RadioItems(id='resolution',
		options=[
			{'label': '1m', 'value': '1'},
			{'label': '5m', 'value': '5'},
			{'label': '30m', 'value': '30'},
			{'label': '1H', 'value': '60'},
			{'label': '6H', 'value': '360'},
			{'label': '12H', 'value': '720'},
			{'label': '1D', 'value': '1440'},
		],
		value='60',
	),

	dcc.Tabs(id="ranges", value='all', children=[
		dcc.Tab(label='ALL', value='all'),
		dcc.Tab(label='1 Hour', value=60),
		dcc.Tab(label='6 Hours', value=360),
		dcc.Tab(label='12 Hours', value=720),
		dcc.Tab(label='1 Day', value=1440),
		dcc.Tab(label='1 Week', value=10080),
		dcc.Tab(label='1 Month', value=43200),
		dcc.Tab(label='6 Months', value=262800),
		dcc.Tab(label='1 Year', value=525600),
	]),

	html.Div(id='output-graph')
	])

@app.callback(
	Output(component_id='output-graph', component_property='children'),
	[Input(component_id='tradingPair', component_property='value'),
	Input(component_id='resolution', component_property='value'),
	Input(component_id='ranges', component_property='value'),]
	)
def update_graph(pair, resolution, span):
	conn, c = db.init('tradingPairs.db')
	data = []
	if span == 'all':
		data = db.getAll(c, pair, resolution)
	else:
		data = db.getSince(c, pair, resolution, span)
	date, close = zip(*data)
	db.close(c, conn)
	return dcc.Graph(id='graph',
		figure ={
			'data': [
				{'x': date, 'y': close, 'type': 'line', 'name': pair}
			],
			'layout': {
				'title': pair
			}
		})

if __name__ == '__main__':
	app.run_server()