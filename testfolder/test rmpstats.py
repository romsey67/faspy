#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 15:21:49 2020

@author: RMS671214
"""
from rmp_stats import *
from scipy.stats import norm
from time import time

x = 0.95

start = time()
abc = norm.ppf(x)
ntime = time()-start
print(ntime, abc)

start = time()
abc = rmpppf(x)
rmptime = time()-start
print(rmptime, abc)

print((rmptime)/ntime)