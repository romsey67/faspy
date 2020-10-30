#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 10:35:20 2020

@author: RMS671214
"""


import rmp_optB73 as b76
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from collections import deque
from time import time
from numpy import datetime64 as dt64
import pandas as pd
from rmp_dates import day_count_factor as day_cf
import scipy


optfile = pd.read_csv('/Users/RMS671214/riskmasterpro/testfolder/OKLI20200715.csv')
optdata = optfile.to_dict(orient='records')


for datum in optdata:
    okli = b76.OptBlack76()
    okli.value_date = dt64(datum['value_date'])
    okli.expiry = dt64(datum['expiry'])
    okli.strike = float(datum['strike'])
    okli.rate_basis = datum['rate_basis']
    okli.day_count = datum['day_count']
    okli.riskfreerate = datum['rate']
    okli.price = datum['futures']
    okli.option_type = datum['poc']
    datum['time'] = day_cf('Actual/365', okli.value_date, okli.expiry)
    try:
        ivol = okli.calc_impliedvol(datum['settlement'])
    except:
        ivol = None
        
    datum['implied_vol'] = ivol
    print(datum['time'], okli.option_type, okli.strike, okli.price,
          datum['settlement'], ivol)

    if ivol is not None:
        okli.volatility = ivol
        values = okli.calculate()
        datum['calc_value'] = values['value']
        datum['delta'] = values['delta']
        datum['gamma'] = values['gamma']
        datum['vega'] = values['vega']
        datum['vanna'] = values['vanna']
    else:
        datum['calc_value'] = None
        datum['delta'] = None
        datum['gamma'] = None
        datum['vega'] = None
        datum['vanna'] = None

#%%

chartdata = [datum for datum in optdata if datum['poc'] == 'put']
exptime = [datum['time'] for datum in chartdata]
settime = set(exptime)
settime = list(settime)
settime.sort()
strikes = [datum['strike'] for datum in chartdata]
strikes = set(strikes)
strikes = list(strikes)
strikes.sort()
print(settime)


zvols = []
for otime in settime:
    vols = []
    for strike in strikes:
        temp = [datum['implied_vol'] for datum in chartdata if (datum['strike'] == strike and datum['time'] == otime)]
        if len(temp) == 0:
            vols.append(np.nan)
        else:
            vols.append(temp[0])
    zvols.append(vols)

test = pd.DataFrame(zvols, index=settime, columns=strikes, dtype=np.float64)
test1 = test.T
test2 = test1.interpolate(method = 'pchip',inplace=False)
newlist = test2.T
mylist = test2.to_dict(orient='list')

#print(np.array(zvols))

#%%



#%%

fig = plt.figure()
ax = Axes3D(fig)

ax.plot_surface(np.array(settime), np.array(strikes), np.array(zvols),spline cmap='viridis', edgecolor='none')
ax.set_title('Surface plot')
plt.show()