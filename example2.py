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

import math
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, \
     nearest_workday, USMartinLutherKingJr, USPresidentsDay, GoodFriday, \
     USMemorialDay, USLaborDay, USThanksgivingDay


# Creating a trading calendar.
class USTradingCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday('New Years Day', month=1, day=1, observance=nearest_workday),
        USMartinLutherKingJr,
        USPresidentsDay,
        GoodFriday,
        USMemorialDay,
        Holiday('Independence Day', month=7, day=4,
                observance=nearest_workday),
        USLaborDay,
        USThanksgivingDay,
        Holiday('Christmas', month=12, day=25, observance=nearest_workday)
    ]


def remove_no_trade_days(dates):
    cal = USTradingCalendar()
    # Remove weekends
    dates = dates[dates.dayofweek < 5]
    # Remove actual holidays
    return dates.difference(cal.holidays(dates[0], dates[len(dates)-1]))


def bollinger_bands(df, stocks):
    for stock in stocks:
        r_mean = df[stock].rolling(center=False, window=15).mean()
        r_std = df[stock].rolling(center=False, window=15).std()
        bb_upper = r_mean + (r_std*2)  # 2 deviations
        bb_lower = r_mean - (r_std*2)

        plot = df[stock].plot(title=stock + " w/ BB", label=stock)
        plot.set_xlabel("Date")
        plot.set_ylabel("Price")
        r_mean.plot(label="Rolling Mean", ax=plot)
        bb_upper.plot(label="Upper Band", ax=plot)
        bb_lower.plot(label="Lower Band", ax=plot)
        plot.legend(loc="best")
        plt.show()


def sharpe_ratio(df, risk_free_rate):
    # Currently assumes 0 for risk free rate and annual sampling
    dr = daily_returns(df)
    print(math.sqrt(252) * (dr.mean()/dr.std()))


def daily_returns(df):
    dr = (df / df.shift(1)) - 1
    dr.ix[0] = 0  # First value should be zero.
    return dr
    # Former plot info that can be used later.
    # if graph_type == "scatter":
    #    dr.plot(kind=graph_type, x="AAPL", y="GOOG")
    #    test, test_two = np.polyfit(dr["AAPL"], dr["GOOG"], 1)
    #    plt.plot(dr["AAPL"], test*dr["AAPL"] + test_two,  '-', color="red")
    # elif graph_type == "hist":
    #    dr.plot(kind="hist", bins=60)
    # else:
    #    dr.plot()
    # plt.show()


def cumulative_returns(df):
    cr = (df.shift(1) / df.ix[0]) - 1
    cr.ix[0] = 0
    return cr


# From beginning of 2012 until today.
start = datetime.datetime(2015, 10, 19)
end = datetime.date(2016, 10, 19)
# end = datetime.date.today()
dates = pd.date_range(start, end)
dates = remove_no_trade_days(dates)

# Hypothetically will support any amount of stocks...
stock_symbols = ["AAPL", "GOOG"]

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

# Fill all stocks for NA values.
for frame in complete_stock_info:
    frame.fillna(method="ffill", inplace=True)
    frame.fillna(method="bfill", inplace=True)

# Plot all of the charts for fun
for frame in complete_stock_info:
    plot = frame[stock_symbols].plot(title=frame.name)
    plt.show()


# Bollinger Bands
# bollinger_bands(stocks_adj, stock_symbols)

# Daily Returns
# daily_returns(stocks_adj, stock_symbols, "scatter")
# cumulative_returns(stocks_adj, stock_symbols)

sharpe_ratio(stocks_adj, 0.0)
