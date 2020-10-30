#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 15:02:42 2020

@author: RMS671214

"""

# ******************************************************************************
#                           THIS IS A TEST MODULE FOR
#   1. STRates class
#   2. LTRates class
#   3. Rates class
#   4. DFactor class
#
# ******************************************************************************
from interestrate.fas_ircls import DFactor, STRates, LTRates, Rates
from numpy import datetime64 as dt64
import pandas as pd

# %%
# >>>>>>>>>>>>>>>>>>>>>
# USing STRates class
# >>>>>>>>>>>>>>>>>>>>>
myst = { '1W': 2.35, '1M': 2.45, '3M': 2.55,
        '6M': 2.65, '12M': 2.75}
strates = STRates()
strates.rate_basis = None
strates.business_day = 'Modified Following'
strates.day_count = 'Actual/365 Fixed'
strates.data = myst
value_date = dt64('2020-03-03')

# %%
# >>>>>>>>>>>>>>>>>>>>>
# USing LTRates class
# >>>>>>>>>>>>>>>>>>>>>
mylt = {'1Y': 2.70, '2Y': 2.80, '3Y': 2.90, '5Y': 3.00, '10Y': 3.10, '30Y': 3.25}
ltrates = LTRates()
ltrates.frequency = None
ltrates.business_day = 'Modified Following'
ltrates.day_count = 'Actual/Actual'
ltrates.data = mylt
print(mylt)

# %%
# >>>>>>>>>>>>>>>>>>>>>
# USing Rates class
# >>>>>>>>>>>>>>>>>>>>>
myrates = Rates()
myrates.strates = strates
myrates.ltrates = ltrates
myrates.date_gen_method = 'Forward from issue date'
myrates.value_date = value_date

# %%
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# generating discount factors using DFactor class
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
myrates.calcdf()
# view the discount factors
my_pd = pd.DataFrame(myrates.df.data)

##
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# use the interpolation capability of DFactor class from Rates class
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
rates = myrates.df.rates
xvalue = 0.75
yvalue = myrates.df.interpolate(xvalue)
rvalue = myrates.interpolate(xvalue)

def test_Rates():
    return myrates



    
