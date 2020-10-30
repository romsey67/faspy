#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 18:11:52 2020

@author: RMS671214
"""
import cashflow as cf
import numpy as np
import interam.np_dateutils01 as npd
from cashflow import Bond


#%%
dates = ['2019-01-10','2019-01-20','2019-12-30']
amount = [10,20,'30']

cfs = cf.Structures()
#cfs.dates = dates
#cfs.amounts = amount
cfs.structures = {'dates': dates, 'amount': amount}

#print(cfs.amounts)


#%%

mybond = {}
mybond['issue_date'] = np.datetime64('2018-10-22')
mybond['value_date'] = np.datetime64('2019-10-22')
mybond['maturity'] = np.datetime64('2028-10-22')
mybond['day_count'] = 'Actual/Actual ICMA'
mybond['frequency'] = 'Semi-Annual'
mybond['business_day'] = 'No Adjustment'
mybond['date_generation'] = npd.date_gen_method[1]
mybond['position'] = 1000000
mybond['coupon'] = 8.00
mybond['type'] = 'Fixed Rate Bond'
mybond['yield'] = 5.00

#%%
bond = Bond(init_value = mybond)
print(bond.day_count)
bond.construct_bond()
bond.calculate()

