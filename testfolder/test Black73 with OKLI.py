#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 13:38:16 2020

@author: RMS671214
"""
# ******************************************************************************
#                           THIS IS A TEST MODULE FOR
#   1. EquityIndexOpt
#   the test incudes the usage of :
#   i. STRates class
#   ii. LTRates class
#   iii. Rates class
#   iv. DFactor class
# ******************************************************************************

import rmp_optB73 as b73
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from time import time
from numpy import datetime64 as dt64
from rmp_irdatacls import DFactor, STRates, LTRates, Rates
import pandas as pd
from matplotlib import pyplot as plt

# %%
# >>>>>>>>>>>>>>>>>>>>>
# STRates class
# >>>>>>>>>>>>>>>>>>>>>

myst = { '1W': 2.35, '1M': 2.45, '3M': 2.55,
        '6M': 2.65, '12M': 2.75}
strates = STRates()
strates.rate_basis = None
strates.business_day = 'Modified Following'
strates.day_count = 'Actual/365 Fixed'
strates.rates = myst
value_date = dt64('2020-06-17')

# %%
# >>>>>>>>>>>>>>>>>>>>>
# LTRates class
# >>>>>>>>>>>>>>>>>>>>>
mylt = { '2Y': 2.80, '3Y': 2.90, '5Y': 3.00, '10Y': 3.10}
ltrates = LTRates()
ltrates.frequency = None
ltrates.business_day = 'Modified Following'
ltrates.day_count = 'Actual/365 Fixed'
ltrates.rates = mylt

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


# %%
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# reading from file
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# okli_data = pd.read_csv("/RMS671214/riskmasterpro/OKLI 20200715.csv")
start = time()
okli = b73.OptBlack76()
okli_data = pd.read_csv(r"OKLI 20200715.csv")
futures = {'July,2020':1_590, 'August,2020':1_585, 'September,2020': 1_577,
           'December,2020':1_563}

myokli = okli_data.to_dict(orient='records')
index = -1
for i in range(0,196,1):
    row = myokli[i]
    
    contract = row['Contract']
    details = contract.split()
    maturity = details[3]
    str_strike = details[4]
    poc = details[2].lower()
    cmonth = details[1]
    matdate = maturity.split('/')
    okli.value_date = dt64('2020-06-15')
    okli.expiry = dt64('-'.join([matdate[2], matdate[1], matdate[0]]))
    okli.strike = float(str_strike.replace(',', ''))
    okli.rate_basis = 'Money Market'
    okli.day_count = 'Actual/365'
    okli.riskfreerate = 10
    okli.price = futures[cmonth]
    
    okli.option_type = poc
    if isinstance(row['Settlement'], str):
        settlement = float(row['Settlement'].replace(',', ''))
    else:
        settlement = row['Settlement']
    #print(i, row, cmonth, okli.price)
    ivol = okli.calc_impliedvol(settlement)
    okli.volatility = ivol
    row['implied_vol'] = ivol
    values = okli.calculate()
    row['calc_value'] = values['value']
    row['delta'] = values['delta']
    row['gamma'] = values['gamma']
    row['vega'] = values['vega']
    row['vanna'] = values['vanna']
    row['poc'] = poc
    row['cmonth'] = cmonth
    row['strike'] = okli.strike
    
print('End==>>', time()-start)

pdivol = pd.DataFrame(myokli)

# %%
from collections import deque

xaxis = deque()
yaxis = deque()
for row in myokli:
    if row['poc'] == 'put':
        if row['cmonth'] == 'August,2020':
            xaxis.append(row['delta'])
            yaxis.append(row['implied_vol'])
    
plt.plot(xaxis, yaxis, label="implied vol")
plt.legend()
plt.show()


# %%
#Test calculation of implied price
okli.option_type = 'call'
iprice = okli.calc_pricefromdelta(-0.25)

print('iprice', iprice)