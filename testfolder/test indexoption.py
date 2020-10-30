#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 13:38:16 2020

@author: RMS671214
"""
import rmp_eqtopt as eqopt
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from time import time
from numpy import datetime64 as dt64

# %%
r = 2.4872610830067208
d = 2.5
strike = 105.00
price = 100.00
vtime = 7/252
vol = 10

start = time()
call1 = eqopt.eq_indexopt_contdiv_bscall(vtime, vol, r, d, price, strike)
put = eqopt.eq_indexopt_contdiv_bsput(vtime, vol, r, d, price, strike)
print('calculation time', time()-start)

start = time()
st = np.linspace(89, 110, 100)
calls = deque()
puts = deque()

for myst in st:
    calls.append(eqopt.eq_indexopt_contdiv_bscall(vtime, vol, r, d, price,
                                                  myst))
    puts.append(eqopt.eq_indexopt_contdiv_bsput(vtime, vol, r, d, price,
                                                myst))

calls = list(calls)
puts = list(puts)

print('Time for array', time()-start)
#plt.plot(st, calls, label="call")
#plt.plot(st, puts, label="put")
#plt.legend()
#plt.show()

# %%
from rmp_eqtopt import eq_indexopt_contdiv as indexopt
vdate = dt64('2020-06-01')
expiry = dt64('2020-06-10')
r = 2.6
rate_basis = 'Money Market'
dc_basis = 'Actual/365'


start = time()
call2 = indexopt(vdate, expiry, price, strike, vol, d, r, rate_basis, dc_basis,
                 poc='call', method='standard')
call3 = indexopt(vdate, expiry, price, strike, vol, d, r, rate_basis, dc_basis,
                 poc='call', method='modified')
put2 = indexopt(vdate, expiry, price, strike, vol, d, r, rate_basis, dc_basis,
                poc='put', method='standard')
put3 = indexopt(vdate, expiry, price, strike, vol, d, r, rate_basis, dc_basis,
                poc='put', method='modified')
print('Time with another calculator', time() - start)

# %%
# Using Class to calculate
myopt = eqopt.EquityIndexOpt()
myopt.value_date = vdate
myopt.expiry = expiry
myopt.rate_basis = rate_basis
myopt.day_count = dc_basis
myopt.dividend = d
myopt.riskfreerate = r
myopt.volatility = vol
myopt.price = price
myopt.strike = strike
myopt.option_type = 'call'

start = time()
callvalues = myopt.calculate()
print('Time with class==>>', time()-start)

start = time()
callivol = myopt.calc_impliedvol(callvalues['value'])
print('Time to calculate implied vol==>>', time()-start)

myopt.option_type = 'put'
putvalues = myopt.calculate()
start = time()
putivol = myopt.calc_impliedvol(putvalues['value'] * 1.1)
print('Time to calculate put implied vol==>>', time()-start, 'Put ivol==>', putivol)


# %%

vols = np.linspace(1, 70, 100)
myopt.option_type = 'put'
putvalue = []
for vol in vols:
    myopt.volatility = vol
    values = myopt.calculate()
    putvalue.append(values['value'])
plt.plot(vols, putvalue, label="put")
plt.legend()
plt.show()




