# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 11:27:30 2016

This is an attempt at Assignment 1 located here:

http://quantsoftware.gatech.edu/MC1-Project-1.

I am not taking the course, so I will be providing my own date ranges for
testing (the assignment takes in a start date and an end date, I will just
give a range).

@author: Ryan Kush
"""

import math
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, \
     nearest_workday, USMartinLutherKingJr, USPresidentsDay, GoodFriday, \
     USMemorialDay, USLaborDay, USThanksgivingDay


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


def sharpe_ratio(df, risk_free_rate):
    # Currently assumes 0 for risk free rate and annual sampling
    dr = daily_returns(df)
    print(math.sqrt(252) * (dr.mean()/dr.std()))


def daily_returns(df):
    dr = (df / df.shift(1)) - 1
    dr.ix[0] = 0  # First value should be zero.
    return dr


def cumulative_returns(df):
    cr = (df.shift(1) / df.ix[0]) - 1
    cr.ix[0] = 0
    return cr


def remove_no_trade_days(dates):
    cal = USTradingCalendar()
    # Remove weekends
    dates = dates[dates.dayofweek < 5]
    # Remove actual holidays
    return dates.difference(cal.holidays(dates[0], dates[len(dates)-1]))


def access_portfolio(dates, stocks, starting_value, allocation):
    # Initial setup & of data frame
    stocks_adj = pd.DataFrame(index=dates, columns=stock_symbols)
    stocks_adj.name = "Adjusted Close"

    # Grab the data from yahoo
    for symbol in stocks:
        df = data.DataReader(symbol, "yahoo", start, end)
        stocks_adj[symbol] = df["Adj Close"]

    # Fill all stocks for NA values.
    stocks_adj.fillna(method="ffill", inplace=True)
    stocks_adj.fillna(method="bfill", inplace=True)

    daily_returns(stocks_adj)
    cumulative_returns(stocks_adj)

# -----------------------------------------------------------------------------
# Define data to access portfolio
# -----------------------------------------------------------------------------

# One year of trading data
start = datetime.datetime(2015, 10, 19)
end = datetime.date(2016, 10, 19)
dates = pd.date_range(start, end)
dates = remove_no_trade_days(dates)

# Stocks we want to access
stock_symbols = ["AAPL", "GOOG"]

# How much initial money did we put in?
starting_value = 1000000

# How much of the starting value did you put into each stock?
allocation = [.5, .5]

# Access the portfolio
access_portfolio(dates, stock_symbols, starting_value, allocation)
