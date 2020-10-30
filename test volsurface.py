#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 15:56:50 2020

@author: RMS671214
"""
from math import exp, log, sqrt
from rmp_stats import rmpcdf as cdf, rmpppf as ppf
from scipy.stats import norm
from optionquotes import OptionQuotes
import optionutils as ou
from numpy import datetime64 as dt64

'FX Volatility Smile Construction'
'Dimitri Reiswich, Uwe Wystup'
'April 2020'

# %%






fxspot = 4.20
fxstrike = 4.207005836575425
rate_d = 0.025
rate_f = 0.5 / 100
mytime = 1/12
myvol = 0.1
myfwd = ou.fxfwd(fxspot, rate_d, rate_f, mytime)
print('forward rate==>>', myfwd)
bs = 1

# Unadjusted Deltas
ocall = ou.gk(fxspot, fxstrike, rate_d, rate_f, mytime, myvol, poc=1)
dcall = ou.spotdelta(fxspot, fxstrike, rate_d, rate_f, mytime, myvol, poc=1)
oput = ou.gk(fxspot, fxstrike, rate_d, rate_f, mytime, myvol, poc=-1)
dput = ou.spotdelta(fxspot, fxstrike,rate_d, rate_f, mytime, myvol, poc=-1)
parity = dcall - dput
print('no parity with spot delta', parity)


dfcall = ou.fwddelta(fxspot, fxstrike, rate_d, rate_f, mytime, myvol, poc=1)
dfput = ou.fwddelta(fxspot, fxstrike, rate_d, rate_f, mytime, myvol, poc=-1)
print('parity with forward delta', dfcall - dfput)



print('spot delta==>>', dcall, 'forward delta==>', dfcall, fxstrike)
strike_spdelta = ou.strikefrspotdelta(fxspot, dcall, rate_d, rate_f, mytime,
                                      myvol, poc=1)
print('calculated strike from spot delta ==>>', strike_spdelta)
strike_fwddelta = ou.strikefrfwddelta(fxspot, dfcall, rate_d, rate_f, mytime,
                                   myvol, poc=1)

print('calculated strike from fwd delta ==>>', strike_fwddelta)

# %%


pa_fdelta = ou.pafwddelta(fxspot, fxstrike, rate_d, rate_f, mytime, myvol, poc=-1)
print('premium adjusted forward delta==>', pa_fdelta)



strike_pfdelta = ou.nr_4strikefrpafwddelta(fxspot, pa_fdelta, rate_d, rate_f,
                                        mytime, myvol, poc=-1)
print('Newton Raphson on strike from pafdelta==>', strike_pfdelta)
    
# %%
# Defining Market data

optiondata = []
oq = OptionQuotes()
oq.ccypair = 'EUR/USD'
oq.fxspot = 1.3088
oq.erate_d = float(0.3525 / 100)
oq.erate_f = 2.0113 / 100
oq.atm_vol = 21.6215 / 100
oq.rr25_vol = -0.5 / 100
oq.strangle25_vol = 0.7375 / 100
oq.delta_type = 0
oq.atm_delta_convention = 1
optiondata.append(oq)

oq = OptionQuotes()
oq.ccypair = 'USD/JPY'
oq.fxspot = 90.68
oq.erate_d = 0.42875/100
oq.erate_f = 0.3525/100
oq.atm_vol = 21.00/100
oq.rr25_vol = -5.3 / 100
oq.strangle25_vol = 0.184/100
oq.delta_type = 2
oq.atm_delta_convention = 1
optiondata.append(oq)

# %% 
# ATM
opt = optiondata[0]
#opt.calc_time(dt64('2020-06-17'), '1M')
opt.time = 1/12
strike_atm = opt.strike_atm(0.5)
print(opt.ccypair, strike_atm)

opt = optiondata[1]
opt.time = 1/12
#opt.calc_time(dt64('2020-06-17'), '1M')
strike_atm = opt.strike_atm(0.5)
print(opt.ccypair, strike_atm)

# %%
# RR

opt = optiondata[0]
call25 = opt.strike_rr(0.25)
print('call', opt.ccypair, call25)
put25 = opt.strike_rr(-0.25, poc=-1)
print('put', opt.ccypair, put25)

opt = optiondata[1]
call25 = opt.strike_rr(0.25)
print('call', opt.ccypair, call25)
put25 = opt.strike_rr(-0.25, poc=-1)
print('put', opt.ccypair, put25)




    