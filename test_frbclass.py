#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 18:11:52 2020

@author: RMS671214
"""
from ir_class.frbclass import  FRN
from numpy import datetime64 as dt64
from interam.np_dateutils01 import date_gen_method as dg_method
import pandas as pd

pd.set_option('display.max_columns', None)



#%%
mybond = FRN()
errorlist = []
try:
    
    mybond.issue_date = dt64('2018-10-22')
    mybond.value_date = dt64('2020-12-22')
    mybond.maturity = dt64('2028-10-22')
    mybond.day_count = 'Actual/365 Fixed'
    mybond.frequency = 'Semi-Annual'
    mybond.business_day = 'No Adjustment'
    mybond.date_gen = dg_method[1]
    mybond.position = '1_250_000'
    mybond.coupon = 8.00
    mybond.ytm = 4.00
    mybond.bondtype = 'Fixed Rate Bond'
    
except ValueError as myerror:
    errorlist.append(str(myerror))
    #print(myerror)
    
if len(errorlist)>0:
    print(errorlist)
#%%

mybond.construct_bond()
abc = mybond.active_structures
pddata = pd.DataFrame(abc)