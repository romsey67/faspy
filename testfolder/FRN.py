#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 18:11:52 2020

@author: RMS671214
"""
from bondclass import FRN
from numpy import datetime64 as dt64
from rmp_dates import date_gen_method as dg_method
import pandas as pd
import test_generatestdf as tgstdf

pd.set_option('display.max_columns', None)



#%%
mybond = FRN()
errorlist = []
try:
    mybond.ccy = 'MYR'
    mybond.isin = 'ISIN0001'
    mybond.rating = 'AAA'
    mybond.rating_agency = 'RAM'
    mybond.valuation_curve = 'Test Curve'
    mybond.var_curve = 'Test Curve'
    mybond.issuer = 'JPJ Holdings'
    mybond.issue_date = dt64('2020-06-17')
    mybond.value_date = dt64('2020-06-17')
    mybond.maturity = dt64('2022-06-17')
    mybond.day_count = 'Actual/365 Fixed'
    mybond.frequency = 'Quarterly'
    mybond.business_day = 'No Adjustment'
    mybond.date_gen = dg_method[1]
    mybond.face_value = '10_000_000'
    mybond.margin = 1.5
    mybond.spread = 1.5
    mybond.current_coupon = 4.65

except ValueError as myerror:
    errorlist.append(str(myerror))
    #print(myerror)
    
if len(errorlist)>0:
    print(errorlist)
    
# constructing the bond structure 
mybond.construct_bond()
# viewing the structure - somehow, not displaying all the columns
pd_full = pd.DataFrame(mybond.full_structures)
pd_active = pd.DataFrame(mybond.active_structures)
df = tgstdf.getDF()

# %%
try:
    mybond.calculate(df)
except ValueError as myerror:
    errorlist.append(str(myerror))
    print(myerror)

# print(mybond.risk_stats)
pdfrn = pd.DataFrame(mybond.active_structures)
print()

