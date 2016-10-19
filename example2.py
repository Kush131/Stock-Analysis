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


def daily_returns(df, stocks):
    ((df / df.shift(1) - 1)*100).plot()
    plt.show()


def cumulative_returns(df, stocks):
    ((df.shift(1) / df.ix[0] - 1)*100).plot()
    plt.show()


# From beginning of 2012 until today.
start = datetime.datetime(2010, 10, 19)
end = datetime.date.today()
dates = pd.date_range(start, end)
dates = remove_no_trade_days(dates)

# TODO: Remove holidays of trading calendar.

# Hypothetically will support any amount of stocks...
stock_symbols = ["AAPL"]

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

# Plot all of the charts for fun
for frame in complete_stock_info:
    plot = frame[stock_symbols].plot(title=frame.name)
    plt.show()


# Bollinger Bands
bollinger_bands(stocks_adj, stock_symbols)

# Daily Returns
daily_returns(stocks_adj, stock_symbols)
cumulative_returns(stocks_adj, stock_symbols)
