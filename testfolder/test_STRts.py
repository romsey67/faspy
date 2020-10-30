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
from ir_class.irdatacls import STRt
from numpy import datetime64 as dt64
import pandas as pd

# %%
# >>>>>>>>>>>>>>>>>>>>>
# USing STRt class
# >>>>>>>>>>>>>>>>>>>>>
myst = {'T/N': 2.30, 'S/N': 2.33, '1W': 2.35, '1M': 2.45, '3M': 2.55,
        '6M': 2.65, '12M': 2.75}
# myst = {'S/N': 2.33, '1W': 2.35, '1M': 2.45, '3M': 2.55,
#        '6M': 2.65, '12M': 2.75}
strates = STRt()
strates.rate_basis = 'Money Market'
strates.business_day = 'Modified Following'
strates.day_count = 'Actual/365'
strates.start_basis = 'Same Day'
strates.current_date = dt64('2020-06-19')
strates.data = myst

result = strates.calcdf()


pdresult = pd.DataFrame(result)




