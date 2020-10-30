#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 15:20:04 2020

@author: RMS671214
"""
from ir_class.moneymarket import FRADeal
from irdatacls import DFactor, STRates,LTRates,Rates
from numpy import datetime64 as dt64
from interam.curves import generate_st_df_v1_00 as calc_stdf

#%%
#***************************************************************************
#
#                       SETTING UP THE FRA 
#
#**************************************************************************
myfra = FRADeal()
errorlist = []
try:
    myfra.ccy = 'MYR'
    myfra.counterparty = 'Maybank'
    myfra.islending = True
    myfra.ref_no = 'FRA001'
    myfra.start_date = dt64('2020-03-03')
    myfra.maturity = dt64('2020-06-03')
    myfra.principal = 1_000_000.00
    myfra.value_date = dt64('2020-01-23')
    myfra.rate = '2.60'
    myfra.day_count = 'Actual/365 Fixed'
    myfra.islending = False
except ValueError as myerror:
    errorlist.append(str(myerror))
    print('exception: ',str(myerror))

value_date = myfra.value_date
if len(errorlist) > 0:
    print(errorlist)

#%%
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Preparing STRates class for Rates class
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
myst = {'O/N': 2.30, '1W': 2.35, '1M': 2.45, '3M':2.55, '6M': 2.65, '12M': 2.75}
strates = STRates()
try:
    strates.rate_basis = None
    strates.business_day = 'Modified Following'
    strates.day_count = 'Actual/365 Fixed'
    strates.data = myst
except ValueError as myerror:
    errorlist.append(str(myerror))
    print('exception: ',str(myerror))



#%%
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Preparing LTRates class for Rates class
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
mylt = {'1Y': 2.70, '2Y': 2.80, '3Y': 2.90, '5Y':3.00, '10Y': 3.10, '30Y': 3.25}
ltrates = LTRates()

try:
    ltrates.frequency = None
    ltrates.business_day = 'Modified Following'
    ltrates.day_count = 'Actual/365 Fixed'
    ltrates.data = mylt
except ValueError as myerror:
    errorlist.append(str(myerror))
    print('exception: ',str(myerror))
#%%
#>>>>>>>>>>>>>>>>>>>>>
# USing Rates class
#>>>>>>>>>>>>>>>>>>>>>
myrates = Rates()
myrates.strates = strates
myrates.ltrates = ltrates
myrates.date_gen_method = 'Forward from issue date'
myrates.value_date = value_date


# Rates calss has method to generate discount factors
myrates.calcdf()
# discount factors are kept a property 'df' an is a DFactor class object
# printing the discount factors to terminal
#print('Discount Factors ==>', myrates.df.dfs)
#%%

fra_value =myfra.value(discount_curve = myrates.df)
print('FRA Value ==>',fra_value)

fra_settlement = myfra.settlement_value(2.00)
print('FRA Settlement Value ==>',fra_settlement)





