# cryptoPrice
A cyptocurrency price viewing webapp.

Prices come from the market binance.com.

# Getting the data
Run scrape.py on the server to continuosly update the sqlite3 database of price history. 
You will need to fill in API keys in keys.py in order to run scrape.py.
Alternatively, you can download a prepopulated database.

# Running the front end
Run dashboard.py, then go to localhost:8050 in a browser to view the dashboard.
