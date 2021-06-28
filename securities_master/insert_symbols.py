"""
Alpaca API - extract available assets (good enough for now)
yfinance wrapper (ideally i'd use the Alpha Vantage API but the max req per day is 500)
"""

import os
import json
import logging
logging.basicConfig(filename='logfile.log', filemode='w', level=logging.DEBUG)

from securities_master.mysql_instance import connect_mysql_instance

from alpaca_trade_api.rest import REST
import alpaca_trade_api
import yfinance as yf

from dotenv import load_dotenv
load_dotenv()

#Connect to MySQL instance
cnx, cursor = connect_mysql_instance()

# Connect to Alpaca API
api = alpaca_trade_api.REST(os.environ.get('ALPACA_PUBLIC_KEY'),
                            os.environ.get('ALPACA_PRIVATE_KEY'),
                            os.environ.get('ALPACA_PAPER_URL'))

# Use Alpaca API to list_assets
def get_tickers():
    tickers = []
    for asset in api.list_assets():
        if asset.status == 'inactive':
            continue
        ticker = asset.symbol
        ticker = ticker.replace('.', '-')
        tickers.append(ticker)
    return tickers

# Use yfinance to get symbol data
def get_symbol_data():
    tickers = get_tickers()
    symbols = []
    sql_columns = ['ticker',
                   'instrument',
                   'exchange',
                   'market',
                   'name',
                   'sector',
                   'industry',
                   'currency']
    
    json_keys = ['symbol',
                 'quoteType',
                 'exchange',
                 'market',
                 'longName',
                 'sector',
                 'industry',
                 'currency']
    
    for ticker in tickers:
        try:
            ticker_info = yf.Ticker(ticker).info
        except Exception as e:
            logging.info(e)
        
        ticker_dict = {} # fill dict
        for k, v in zip(sql_columns, json_keys):
            try:
                ticker_dict[k] = ticker_info[v]
            except Exception as e:
                logging.info(e)
        
        symbols.append(ticker_dict)
    
    return symbols

symbols = get_symbol_data()




