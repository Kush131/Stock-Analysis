# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 12:16:51 2016

@author: Ryan Kush

Blog post tutorials are cool. So I decided to follow the tutorial from here:
ntguardian.wordpress.com/2016/09/19/introduction-stock-market-data-python-1/
along with the Udacity's course "Machine Learning w/ Trading".
"""

import datetime
import matplotlib.pyplot as plt
from pandas_datareader import data

start = datetime.datetime(2016, 1, 1)
end = datetime.date.today()

apple = data.DataReader("AAPL", "yahoo", start, end)

print(apple.head())

apple["Adj Close"].plot(grid=True)
plt.show()
