#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 10:51:09 2020

@author: RMS671214

"""

from conventions import date_gen_method
import bond_helper as bh
from numpy import datetime64 as dt64
import pandas as pd
import test_DFactor as test
import time

frn_dict = {}
frn_dict['issue_date'] = dt64('2020-06-17', 'D')
frn_dict['maturity'] = dt64('2022-06-17', 'D')
frn_dict['value_date'] = dt64('2020-06-17', 'D')
frn_dict['date_generation'] = date_gen_method[1]
frn_dict['frequency'] = 'Semi-Annual'
frn_dict['day_count'] = 'Actual/365'
frn_dict['business_day'] = 'No Adjustment'
frn_dict['face_value'] = 10_000_000
frn_dict['margin'] = 1.50
frn_dict['spread'] = 1.50
frn_dict['current_coupon'] = 5.5
frn_dict['fixing_basis'] = 'Same Day'
frn_dict['average_period'] = 1

# %%
start = time.time()
bh.construct_frn(frn_dict)
#print(frn_dict['full_structures'])
pdfrn = pd.DataFrame(frn_dict['active_structures'])
print ('Time to construct FRN', time.time()-start)

# %%
start = time.time()
bh.frn_price(frn_dict, test.test_df())
pdfrn2 = pd.DataFrame(frn_dict['active_structures'])
print(frn_dict['proceed'],frn_dict['pvbp01'])
print ('Time to value FRN', time.time()-start)