#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 13:38:16 2020

@author: RMS671214
"""
import rmp_garman_kolhagen as gk
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from time import time
from numpy import datetime64 as dt64


# %%
# Using Class to calculate
myopt = gk.GarmanKolhagen()
myopt.value_date = dt64('2020-07-15', 'D')
myopt.spot_date = dt64('2020-07-17', 'D')
myopt.expiry = dt64('2020-07-30', 'D')
myopt.delivery_date = dt64('2020-08-02', 'D')
myopt.rate_basis = 'Money Market'
myopt.day_count = 'Actual/365'
myopt.rate = 2.5
myopt.volatility = 10
myopt.price = 1590
myopt.strike = 1480
myopt.rate_base = 0.25
myopt.rate_basis_base = 'Money Market'
myopt.day_count_base = 'Actual/360'

myopt.option_type = 'call'

start = time()
callvalues = myopt.calculate()
print('Time with class==>>', time()-start)

start = time()
callivol = myopt.calc_impliedvol(0.1)
print('Time to calculate implied vol==>>', time()-start, callivol)

myopt.option_type = 'put'
putvalues = myopt.calculate()
start = time()
putivol = myopt.calc_impliedvol(putvalues['value'] * 1.1)
print('Time to calculate put implied vol==>>', time()-start, 'Put ivol==>', putivol)


# %%

vols = np.linspace(80, 120, 100)
myopt.option_type = 'put'
putvalue = []
for vol in vols:
    #myopt.volatility = vol
    myopt.price = vol
    values = myopt.calculate()
    putvalue.append(values['vanna'])
plt.plot(vols, putvalue, label="put")
plt.legend()
plt.show()




