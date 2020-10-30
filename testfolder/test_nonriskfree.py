#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 15:02:42 2020

@author: RMS671214

"""

#******************************************************************************
#                           THIS IS A TEST MODULE FOR
#   1. STRates class
#   2. LTRates class
#   3. Rates class
#   4. DFactor class
#
#******************************************************************************
from ir_class.irdatacls import DFactor,STRates,LTRates, Rates
from numpy import datetime64 as dt64
import pandas as pd

#%%
#>>>>>>>>>>>>>>>>>>>>>
# USing STRates class
#>>>>>>>>>>>>>>>>>>>>>
myst = {'O/N': 2.80, '1W': 2.85, '1M': 2.95, '3M':3.05, '6M': 3.20, '12M': 3.3}
strates = STRates()
strates.rate_basis = None
strates.business_day = 'Modified Following'
strates.day_count = 'Actual/365 Fixed'
strates.data = myst
value_date = dt64('2020-03-03')

#%%
#>>>>>>>>>>>>>>>>>>>>>
# USing STRates class
#>>>>>>>>>>>>>>>>>>>>>
mylt = {'1Y': 3.30, '2Y': 3.5, '3Y': 3.6, '5Y':4.2, '10Y': 4.8, '30Y': 5.50}
mylt2 = {'1Y': 3.20, '2Y': 3.3, '3Y': 3.4, '5Y':33.5, '10Y': 3.6, '30Y':3.75}
ltrates = LTRates()
ltrates.frequency = None
ltrates.business_day = 'Modified Following'
ltrates.day_count = 'Actual/365 Fixed'
ltrates.data = mylt

#%%
#>>>>>>>>>>>>>>>>>>>>>
# USing Rates class
#>>>>>>>>>>>>>>>>>>>>>
myrates = Rates()
myrates.strates = strates
myrates.ltrates = ltrates
myrates.date_gen_method = 'Forward from issue date'
myrates.value_date = value_date

#%%
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#generating discount factors using DFactor class
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
myrates.calcdf()
#view the discount factors
my_pd = pd.DataFrame(myrates.df.data)

##
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# use the interpolation capability of DFactor class from Rates class
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
xvalue = 0.75
yvalue = myrates.df.interpolate(xvalue)

def test_Rates():
    return myrates



    
