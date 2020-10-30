#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 15:23:49 2020

@author: RMS671214
"""
import QuantLib as ql

def print_curve(xlist, ylist, precision=3):
    """
    Method to print curve in a nice format
    """
    print("----------------------")
    print("Maturities\tCurve")
    print("----------------------")
    for x,y in zip(xlist, ylist):
        print (x,"\t\t", round(y, precision))
    print("----------------------")
    
# Deposit rates
depo_maturities = [ql.Period(6,ql.Months), ql.Period(12, ql.Months)]
depo_rates = [20.25, 20.5]

# Bond rates
bond_maturities = [ql.Period(6*i, ql.Months) for i in range(3,30)]
bond_rates = [10.75, 11.0, 11.25, 11.5, 11.75, 11.80, 12.00, 12.1, 12.15, 
              12.2, 12.3, 12.35, 12.4, 12.5, 12.6, 12.6, 12.7, 12.8]

print_curve(depo_maturities+bond_maturities, depo_rates+bond_rates)

# %%
print(depo_maturities)
print(bond_maturities)

#%% 
lt_mat = [ql.Period("1Y6M"), ql.Period("2Y"), ql.Period("3Y"),
          ql.Period("5Y"), ql.Period("7Y"), ql.Period("10Y"),
          ql.Period("15Y"), ql.Period("20Y"), ql.Period("30Y")]
lt_rates = [20.75, 21.0, 21.25, 21.5, 21.75, 21.80, 22.00, 22.1, 22.15]
# %%

calc_date = ql.Date(15, 1, 2020)
ql.Settings.instance().evaluationDate = calc_date

calendar = ql.UnitedStates()
bussiness_convention = ql.Unadjusted 
day_count = ql.Thirty360()
end_of_month = True
settlement_days = 0
face_amount = 100
coupon_frequency = ql.Period(ql.Semiannual)
settlement_days = 0

# %%
# create deposit rate helpers from depo_rates
depo_helpers = [ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(r/100.0)), 
                                     m, 
                                     settlement_days, 
                                     calendar, 
                                     bussiness_convention, 
                                     end_of_month, 
                                     day_count ) 
                for r, m in zip(depo_rates, depo_maturities)]

# %%
# create fixed rate bond helpers from fixed rate bonds
bond_helpers = []
for r, m in zip(lt_rates, lt_mat):
    termination_date = calc_date + m
    schedule = ql.Schedule(calc_date,
                   termination_date, 
                   coupon_frequency, 
                   calendar,
                   bussiness_convention, 
                   bussiness_convention, 
                   ql.DateGeneration.Backward, 
                   end_of_month)
    
    bond_helper = ql.FixedRateBondHelper(ql.QuoteHandle(ql.SimpleQuote(face_amount)),
                                        settlement_days,
                                        face_amount,
                                        schedule,
                                        [r/100.0],
                                        day_count,
                                        bussiness_convention,
                                        )
    bond_helpers.append(bond_helper)
    
# %%
# The yield curve is constructed here
rate_helpers = depo_helpers + bond_helpers
yieldcurve = ql.PiecewiseLogCubicDiscount(calc_date,
                             rate_helpers,
                             day_count)
# print(yieldcurve)


# %%
# get spot rates
spots = []
tenors = []
for d in yieldcurve.dates():
    yrs = day_count.yearFraction(calc_date, d)
    compounding = ql.Compounded
    freq = ql.Semiannual
    zero_rate = yieldcurve.zeroRate(yrs, compounding, freq)
    df = yieldcurve.discount(yrs, d)
    print(df)
    tenors.append(yrs)
    eq_rate = zero_rate.equivalentRate(day_count, 
                                       compounding, 
                                       freq, 
                                       calc_date, 
                                       d).rate()
    spots.append(100*eq_rate)
    
# %%
print_curve(tenors, spots)