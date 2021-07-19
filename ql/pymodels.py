from ql.ql_enums import *

from pydantic import BaseModel, validator
from typing import List
from numpy import datetime64 as dt64


class Rate(BaseModel):
    tenor: str
    rate: float

    @validator('tenor')
    def valid_tenor(cls, v):
        prd = v[-1]
        number = v[:len(v)-1]
        if prd not in ['d', 'D', 'w', 'W', 'm', 'M']:
            raise ValueError('not a valid period')
        else:
            try:
                x = int(number)
            except:
                raise ValueError('not a valid period')
        return  v

    @validator('rate')
    def valid_rate(cls, v):
        
        try:
            x = float(v)
        except:
            raise ValueError('rate must be a number')
        return  v


class Holiday(BaseModel):
    date: str

    @validator('date')
    def valid_rate(cls, v): 
        try:
            thedate = dt64(v)
        except:
            raise ValueError('not a valid date format for Holidays')
        return  v


class DepoSetting(BaseModel):
    start_basis: StartBasis = StartBasis.today
    business_day: BusinessDay = BusinessDay.no_adjustment
    day_count: DayCount = DayCount.act_act_act365
    eom: bool = False

    @validator('start_basis')
    def valid_start_basis(cls, v): 
        if v not in StartBasis:
            raise ValueError
        return  v

class BondSetting(BaseModel):
    start_basis: StartBasis = StartBasis.today
    day_count: DayCount = DayCount.act_act_act365
    pmt_day_count: DayCount = DayCount.act_act_act365
    


