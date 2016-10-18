"""
Created on Mon Oct 17 17:35:18 2016

@author: Ryan Kush

Playing around with stock info is fun. I have been taking the Udacity
course "Machine Learning for Trading" and following some blog posts
on using Python for stock analysis, so I have combined the two for a mini
project. This particular example is just me combining the course with the
blog posts I have read since the Udacity course exports data from CSV files
instead of pulling information from the web.

Usage: Put stock symbols you would like to plot inside of "stock symbols".
The script will gather all the info from Yahoo Finance and plot out stocks
in comparison to eachother according to the six categories on YF: Open,
High, Low, Close, Volume, and Adjusted Close.
"""

import datetime
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data

# From beginning of 2012 until today.
start = datetime.datetime(2012, 10, 18)
end = datetime.date.today()
dates = pd.date_range(start, end)

# Hypothetically will support any amount of stocks...
stock_symbols = ["AAPL", "NFLX", "FB"]

stocks_open = pd.DataFrame(index=dates, columns=stock_symbols)
stocks_open.name = "Open"
stocks_high = pd.DataFrame(index=dates, columns=stock_symbols)
stocks_high.name = "High"
stocks_low = pd.DataFrame(index=dates, columns=stock_symbols)
stocks_low.name = "Low"
stocks_close = pd.DataFrame(index=dates, columns=stock_symbols)
stocks_close.name = "Close"
stocks_vol = pd.DataFrame(index=dates, columns=stock_symbols)
stocks_vol.name = "Volume"
stocks_adj = pd.DataFrame(index=dates, columns=stock_symbols)
stocks_adj.name = "Adjusted Close"

complete_stock_info = [stocks_open, stocks_high,
                       stocks_low, stocks_close,
                       stocks_vol, stocks_adj]

for symbol in stock_symbols:
    df = data.DataReader(symbol, "yahoo", start, end)
    stocks_open[symbol] = df["Open"]
    stocks_high[symbol] = df["High"]
    stocks_low[symbol] = df["Low"]
    stocks_close[symbol] = df["Close"]
    stocks_vol[symbol] = df["Volume"]
    stocks_adj[symbol] = df["Adj Close"]

for frame in complete_stock_info:
    frame[stock_symbols].plot(title=frame.name)
    plt.show()
