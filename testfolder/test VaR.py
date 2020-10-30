#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 17:03:03 2020

@author: RMS671214
"""


from investpy.stocks import get_stock_historical_data as stockdata
from collections import deque
from numpy import array as arr, corrcoef, cov, nanstd, isnan
from math import sqrt, log, exp
import json
#import rmp_stats

def get_stockhistdata(stock, country, startdate, enddate):
    sdate = str(startdate)
    sdates = sdate.split('-')
    sdates.reverse()
    fdate = '/'.join(sdates)

    edate = str(enddate)
    edates = edate.split('-')
    edates.reverse()
    tdate = '/'.join(edates)
    hdata = stockdata(stock, country, as_json=True, from_date=fdate, to_date=tdate, order='ascending', interval='Daily')
    h_data = json.loads(hdata)
    data = h_data['historical']
    datalen = len(data)
    
    for i in range(datalen):
        datum = data[i]
        tempdate = datum['date']
        tempdates = tempdate.split('/')
        tempdates.reverse()
        newdate = '-'.join(tempdates)
        datum['date'] = newdate

    return (data)


def api_calc_vol(data,hperiod=1):

    def myFunc(datum):
        return datum['date']
    data.sort(reverse=True, key=myFunc)

    datalen = len(data)
    logret = deque()
    for i in range(datalen-hperiod):
        datum = data[i]
        datum['return']= log(datum['close']/data[i + hperiod]['close']) * 100
        logret.append(datum['return'])

    npret = arr(logret)
    vol = nanstd(npret)
    return (data, vol)

def api_twostockdata(stock1, stock2, startdate, enddate):

    country = 'United States'
    stocks = []
    stock1 = get_stockhistdata(stock1, country, startdate, enddate)
    data, vol = api_calc_vol(stock1, hperiod=1)
    apple = {'data': data, 'vol':vol}
    stocks.append(data)
    apple['var'] = 1.645 * apple['vol'] * 0.01 * 351.59
    print('apple var ==>>', apple['var'])

    stock2 = get_stockhistdata(stock2, country, startdate, enddate)
    data, vol = api_calc_vol(stock2, hperiod=1)
    ford = {'data': data, 'vol':vol}
    ford['var'] = 1.645 * ford['vol'] * 0.01 * 1.33 * 264
    print('ford var ==>>', ford['var'])


    stocks.append(data)

    
    correl = twostockscorrel(stocks)

    var = sqrt(pow(apple['var'],2) + pow(ford['var'],2) + 2 * correl * apple['var'] * ford['var'])
    print('Simple VaR ==>>', var)

    return {'apple':apple, 'ford': ford, 'correl':correl}


def twostockscorrel(stocks):
    #print(stocks[0])
    return1 = arr([datum['return'] * 0.01 for datum in stocks[0] if datum.get('return') is not None])
    return2 = arr([datum['return'] * 0.01 for datum in stocks[1] if datum.get('return') is not None])
    returns = arr([return1, return2])
    correl = corrcoef(returns)
    print('Correl',correl)
    cova = cov(returns)
    asset1 = arr([351.59, 264 * 1.33])
    wcov = (asset1.dot(cova))
    var = 1.65 * sqrt((wcov.dot(asset1.transpose())))
    print('var==>>',var)
    return correl[0][1]


apple = 'AAPL'
ford = 'FORD'

result = api_twostockdata(apple, ford, '17/06/2019', '17/06/2020')
