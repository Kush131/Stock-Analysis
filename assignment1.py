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
from pandas_datareader import data
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, \
     nearest_workday, USMartinLutherKingJr, USPresidentsDay, GoodFriday, \
     USMemorialDay, USLaborDay, USThanksgivingDay


class USTradingCalendar(AbstractHolidayCalendar):
        rules = [
            Holiday('New Years Day', month=1, day=1,
                    observance=nearest_workday),
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


def create_trading_calendar(start, end):
    dates = pd.date_range(start, end)
    cal = USTradingCalendar()
    # Remove weekends
    dates = dates[dates.dayofweek < 5]
    # Remove actual holidays
    return dates.difference(cal.holidays(dates[0], dates[len(dates)-1]))


class stock:
    symbol = None  # The stock symbol
    volume = None  # How much of the stock we own
    start = None  # The beginning of our stock pricing
    end = None   # The end of our stock pricing
    df = None  # The dataframe with our stock data

    def __init__(self, symbol, vol, start, end):
        self.symbol = symbol
        self.volume = vol
        self.start = start
        self.end = end
        dates = create_trading_calendar(start, end)
        self.df = pd.DataFrame(index=dates, columns=[symbol])
        df = data.DataReader([symbol], "yahoo", start, end)
        self.df[symbol] = df["Adj Close"]
        self.df.ffill(inplace=True)
        self.df.bfill(inplace=True)

    def daily_returns(self):
        dr = (self.df / self.df.shift(1)) - 1
        dr.ix[0] = 0  # First value should be zero.
        return dr

    def cumulative_returns(self):
        cr = (self.df.shift(1) / self.df.ix[0]) - 1
        cr.ix[0] = 0
        return cr

    def sharpe_ratio(self, risk_free_rate):
        # Currently assumes 0 for risk free rate and annual sampling
        dr = stock.daily_returns(self.df)
        print(math.sqrt(252) * (dr.mean()/dr.std()))

    def asset_value(self):
        return self.volume * self.df


class portfolio:
    stocks = []
    allocation = []

# -----------------------------------------------------------------------------
# Define data to access portfolio
# -----------------------------------------------------------------------------

# One year of trading data
start = datetime.datetime(2015, 10, 19)
end = datetime.date(2016, 10, 19)

google = stock("GOOG", 2, start, end)
print(google.daily_returns().plot())
print(google.cumulative_returns().plot())
print(google.asset_value().plot())
