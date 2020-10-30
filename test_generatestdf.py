#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 15:52:34 2020

@author: RMS671214
"""
from rmp_curves import generate_st_df as gen_stdf
from time import time
from numpy import datetime64 as dt64
import pandas as pd
from rmp_curves import generate_fulldf as genfdf
from matplotlib import pyplot as plt

start = time()
value_date = dt64('2020-06-17', 'D')
day_count = 'Actual/365'
business_day = "Modified Following"
rate_basis = 'Money Market'

myst = {'1W': 2.90, '2W':2.95, '3W': 3.00, '1M': 3.05, '2M':3.10, '3M': 3.15,
        '4M': 3.225, '5M': 3.20, '6M': 3.30, '9M': 3.35, '12M': 3.40}
stdf = gen_stdf(value_date, myst, day_count, business_day,
                rate_basis=rate_basis, holidays=[])

print('Time to generate stdf==>>', time()-start)
pddf = pd.DataFrame(stdf)

# %%
from rmp_irdatacls import STRates

start = time()
strates = STRates()
strates.rate_basis = rate_basis
strates.business_day = business_day
strates.day_count = day_count
strates.rates = myst
strates.start_date = value_date
result = strates.calc_df()
print('Time to generate stdf using STRates==>>', time()-start)

pddf2 = pd.DataFrame(result)
# %%
start = time()
mylt = {'1Y': 3.53, '2Y':3.60, '3Y': 3.70, '4Y': 3.80, '5Y':3.90, '7Y': 4.00,
        '10Y': 4.10, '15Y': 4.20, '20Y': 4.30, '30Y': 4.40}
result = genfdf(value_date, myst, strates.day_count, strates.business_day,
                strates.rate_basis, mylt, day_count, business_day)
print('Time to generate full df ==>>', time()-start)
pddf3 = pd.DataFrame(result)

# %%

xaxis = list(map(lambda x: x['time'], result))
yaxis = list(map(lambda x: x['df'], result))
plt.plot(xaxis[: 7], yaxis[:7])
plt.title('TutorialKart')
plt.show()

# %% 
# >>>>>>>>>>>>>>>>>>>>>
# USing LTRates class
# >>>>>>>>>>>>>>>>>>>>>
from rmp_irdatacls import LTRates
ltrates = LTRates()
ltrates.frequency = 'Semi-Annual'
ltrates.business_day = 'Modified Following'
ltrates.day_count = day_count
ltrates.start_date = value_date
ltrates.rates = mylt


# %%
# >>>>>>>>>>>>>>>>>>>>>
# USing Rates class
# >>>>>>>>>>>>>>>>>>>>>
start = time()
from rmp_irdatacls import Rates
myrates = Rates()
myrates.strates = strates
myrates.ltrates = ltrates
myrates.date_gen_method = 'Forward from issue date'
myrates.value_date = value_date
myrates.calcdf()
print('Time to generate full df with Rates==>>', time()-start)


def getDF():
    return myrates.df