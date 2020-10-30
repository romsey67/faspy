#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 18:11:52 2020

@author: RMS671214
"""
from ir_class.bondclass import  BondIssue
from numpy import datetime64 as dt64
from interam.np_dateutils01 import date_gen_method as dg_method
import pandas as pd

pd.set_option('display.max_columns', None)



#%%
mybond = BondIssue()
errorlist = []
try:
    mybond.ccy = 'MYR'
    mybond.isin = 'ISIN0001'
    mybond.rating = 'AAA'
    mybond.rating_agency = 'RAM'
    mybond.valuation_curve = 'Test Curve'
    mybond.var_curve = 'Test Curve'
    mybond.issuer = 'JPJ Holdings'
    mybond.issue_date = dt64('2018-10-22')
    mybond.value_date = dt64('2021-10-22')
    mybond.maturity = dt64('2028-10-22')
    mybond.day_count = 'Actual/365 Fixed'
    mybond.frequency = 'Semi-Annual'
    mybond.business_day = 'No Adjustment'
    mybond.date_gen = dg_method[1]
    mybond.position = '1_000_000'
    mybond.coupon = 0.00
    mybond.ytm = 1.00
    mybond.bondtype = 'Fixed Rate Bond'
    
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
try:
    mybond.calculate()
except ValueError as myerror:
    errorlist.append(str(myerror))
    print(myerror)
    
print(mybond.risk_stats)
    
