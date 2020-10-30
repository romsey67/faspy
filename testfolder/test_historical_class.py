#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 14:20:03 2020

@author: RMS671214
"""
#%%
#***********************************************************************
#This module is used to test classes in irdatacls
#
#%%
from ir_class.irdatacls import Data, HistoricalData
from numpy import datetime64 as dt64

#%%

rates = {'1M': 2.50,'3M':2.60, '6M': 2.70}
myrate = Data()
myrate.data = rates
myrate.single_data('1M')

date1 = {'2020-01-01': myrate}
myhis = HistoricalData()
myhis.historical = date1
testtenors = myhis.historical['2020-01-01'].data
date2 = {'2020-01-02':myrate}
myhis.addnewdata(date2)

viewdata = myhis.view_data_as_dict()