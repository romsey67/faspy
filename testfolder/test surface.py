#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 19:34:13 2020

@author: RMS671214
"""
import pandas as pd

# %% Data

vols = [{'tenor': '1W',  'atm': 10.00, 'rr25': 1.0, 'rr10': 2.0, 'str25': 2.0,
         'str10': 3.0, 'fly25': 0.5, 'fly10': 1},
        {'tenor': '1M', 'atm': 12.00, 'rr25': 1.5, 'rr10': 2.5, 'str25': 2.5,
         'str10': 3.5, 'fly25': 1.0, 'fly10': 1.5},
        {'tenor': '3M',  'atm': 14.00, 'rr25': 2.0, 'rr10': 3.0, 'str25': 3.0,
         'str10': 4.0, 'fly25': 1.5, 'fly10': 2},
        {'tenor': '6M', 'atm': 16.00, 'rr25': 2.5, 'rr10': 3.5, 'str25': 3.5,
         'str10': 4.5, 'fly25': 2.0, 'fly10': 2.5},
        {'tenor': '12M', 'atm': 20.00, 'rr25': 3.0, 'rr10': 4.0, 'str25': 4.0,
         'str10': 5.0, 'fly25': 2.5, 'fly10': 3.0}]

for vol in vols:
    if vol['tenor'] == '1W':
        vol['time'] = float(1/52)
    elif vol['tenor'] == '1M':
        vol['time'] = float(1/12)
    elif vol['tenor'] == '3M':
        vol['time'] = float(3/12)
    elif vol['tenor'] == '6M':
        vol['time'] = float(6/12)
    elif vol['tenor'] == '12M':
        vol['time'] = float(1.00)

# %% Volatility suface against delta
surface = []
for i in range(len(vols)):
    datum = vols[i]
    vol = {}
    #vol['tenor'] = datum['tenor']
    vol['atm'] = datum['atm']
    vol['time'] = datum['time']
    vol['c25'] = datum['atm'] + 0.5 * datum['rr25'] + datum['str25']
    vol['p25'] = datum['atm'] - 0.5 * datum['rr25'] + datum['str25']
    vol['c10'] = datum['atm'] + 0.5 * datum['rr10'] + datum['str10']
    vol['p10'] = datum['atm'] - 0.5 * datum['rr10'] + datum['str10']
    surface.append(vol)

pd_surf = pd.DataFrame(surface)
pd_surf.reset_index()
pd_surf.set_index('time')

#%% 2nd Method

# %% Volatility suface against delta
surface2 = []
for i in range(len(vols)):
    datum = vols[i]
    vol = {}
    #vol['tenor'] = datum['tenor']
    vol['time'] = datum['time']
    vol['10'] = datum['atm'] + 0.5 * datum['rr10'] + datum['str10']
    vol['25'] = datum['atm'] + 0.5 * datum['rr25'] + datum['str25']
    vol['50'] = datum['atm']
    vol['75'] = datum['atm'] - 0.5 * datum['rr25'] + datum['str25']
    vol['90'] = datum['atm'] - 0.5 * datum['rr10'] + datum['str10']
    surface2.append(vol)

pd_surf2 = pd.DataFrame(surface2)


# %% Copy above data and calculate strike for each delta
import optionutils as ou
rate_d = 0.025
rate_f = 0.005
spot = 4.20
surface3 = []

for datum in surface2:
    newdatum = {}
    for key in datum:
        if key != 'time':
            delta = float(key) * 0.01
            strike = ou.strikefrspotdelta(spot, delta, rate_d, rate_f, datum['time'],
                                  datum[key] * 0.01, poc=1)
            newdatum[key] = strike
        else:
            newdatum['time'] = datum['time']
    surface3.append(newdatum)
            

    
pd_surf3 = pd.DataFrame(surface3)


# %% Lets try charting
deltas = [10, 25, 50, 75, 90]
times = [datum['time'] for datum in surface3]

z = []
for datum in surface3:
    strikes =[]
    for key in datum:
        if key != 'time':
            strikes.append(datum[key])
    z.append(strikes)

from scipy import interpolate    
print(len(deltas), len(times))
f = interpolate.interp2d(deltas, times, z, kind='cubic')
k = f(10, 0.25)
print(k)

# %% We know remaining time and strike
# How do we find vol using interp2d
from math import exp, log

mystrike = 4.30
poc = 1
mytime = 0.33
fwd = spot * exp((rate_d-rate_f) * mytime)

# objective: Find my volatility
# first step interpolate my delta
inc = 1
mydelta = log(fwd/mystrike)
if mydelta < 0:
    mydelta = 75
elif mydelta > 0:
    mydelta = 25
else:
    mydelta = 50

strike0 = float(f(mydelta, mytime))
strike1 = float(f(mydelta + inc, mytime))
der = (strike1-strike0) / inc
#print(strike1, strike0, mydelta, der)
counter = 0
while counter <100:
    #print(counter)
    # print(strike0, mydelta, der)
    mydelta = mydelta - (strike0 - mystrike)/der
    #print('==>',x,cd, value0-x,der, (value0 - x)/der)
    strike0 = float(f(mydelta, mytime))
    strike1 = float(f(mydelta + inc, mytime))
    if abs(strike0 - mystrike) < 0.0000001:
        #print(strike1, strike0, der, abs(strike0 - mystrike))
        counter = 100
    #print('value1', value1, 'value0', value0)
    der = (strike1-strike0)/ inc
    #print(strike1, strike0, der, abs(strike0 - mystrike))
    counter += 1

print('mydeta=>>', mydelta)

# %% Next step find vol from delta
deltas = [10, 25, 50, 75, 90]
times = [datum['time'] for datum in surface2]

zvols = []
for datum in surface2:
    vols =[]
    for key in datum:
        if key != 'time':
            vols.append(datum[key])
    zvols.append(vols)


print(zvols)
f = interpolate.interp2d(deltas, times, zvols, kind='cubic')
k = f(mydelta, mytime)
print(k)



