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

import rmp_eqtopt as eqopt
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
okli = eqopt.EquityIndexOpt()
okli_data = pd.read_csv(r"OKLI 20200715.csv")

myokli = okli_data.to_dict(orient='records')
index = -1
for i in range(125,126,1):
    row = myokli[i]
    
    contract = row['Contract']
    details = contract.split()
    maturity = details[3]
    str_strike = details[4]
    poc = details[2].lower()
    matdate = maturity.split('/')
    okli.value_date = dt64('2020-06-15')
    okli.expiry = dt64('-'.join([matdate[2], matdate[1], matdate[0]]))
    okli.strike = float(str_strike.replace(',',''))
    okli.rate_basis = 'Money Market'
    okli.day_count = 'Actual/365'
    okli.dividend = 0.00
    okli.riskfreerate = 10.00
    okli.price = 1590
    
    okli.option_type = poc
    if isinstance(row['Settlement'], str):
        settlement = float(row['Settlement'].replace(',',''))
    else:
        settlement = row['Settlement']
    ivol = okli.calc_impliedvol(settlement)
    okli.volatility = ivol
    row['implied_vol'] = ivol
    print(i, row, ivol, okli.calculate())
    print('End==>>', time()-start)



# %%

vols = np.linspace(0.1, 10, 100)
callvalue = []
for vol in vols:
    okli.volatility = vol
    values = okli.calculate()
    callvalue.append(values['value'])
plt.plot(vols, callvalue, label="put")
plt.legend()
plt.show()


