#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 17:51:26 2020

@author: RMS671214
"""

from np_dateutils01 import *
from numpy import datetime64 as dt64
import pandas as pd


currentDate = dt64('2020-06-17')
maturity = dt64('2022-06-17')
issueDate = dt64('2020-06-17')
test = generate_dates(currentDate, maturity, issueDate=issueDate, frequency=6,
                   business_day='No Adjustment',
                   method='Forward from issue date',
                   holidays=[])

pddates = pd.DataFrame(test)