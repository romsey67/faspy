#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 10:07:31 2020

@author: RMS671214
"""


from ir_class.discountinstrument import DiscountInstrument, BA,Bill
from numpy import datetime64 as dt64

#%%
#********************************************************************************
#
#   USING BA class. This is a child class of DiscountInstrument
#
#********************************************************************************

myba = BA()
errorlist = []
#use try to trap error from crashing your application
try:
    myba.acceptor = 'Maybank'
    myba.drawer = "Justified SB"
    myba.ba_no = 'BA:01234'
    myba.ccy = 'MYR'
    myba.day_count = 'Actual/365 Fixed'
    myba.face_value = 125_000
    myba.maturity = dt64('2020-06-02')
    myba.value_date = dt64('2020-03-23')
    myba.rate = 'a2.5'
    myba.rate_basis = 'Discount Rate'
except Exception as myerror:
    errorlist.append(str(myerror))
    print('exception: ',str(myerror))
    

print(myba.proceed())

try:
    myvalue = myba.value(2.5,'Money Market')
except ValueError as myerror:
    errorlist.append(str(myerror))

if len(errorlist) == 0  :
    print(myvalue)

if len(errorlist) > 0 :
    print(errorlist)



#%%
#********************************************************************************
#
#   USING Bill class. This is a child class of DiscountInstrument
#
#********************************************************************************



mybill = Bill()
errorlist = []
#use try to trap error from crashing your application
try:
    mybill.issuer = 'Malaysian Government'
    mybill.isin = 'MYT-Bill01'
    mybill.ccy = 'MYR'
    mybill.day_count = 'Actual/365 Fixed'
    mybill.face_value = 1_125_000
    mybill.maturity = dt64('2020-06-02')
    mybill.value_date = dt64('2020-03-23')
    mybill.rate = '2.5'
    mybill.rate_basis = 'Discount Rate'
except Exception as myerror:
    errorlist.append(str(myerror))
    print('exception: ',str(myerror))
    

print(mybill.proceed())

try:
    myvalue = mybill.value(2.5,'Money Market')
except ValueError as myerror:
    errorlist.append(str(myerror))

if len(errorlist) == 0  :
    print(myvalue)

if len(errorlist) > 0 :
    print(errorlist)


#%%    
    
print (isinstance(mybill,Bill))




