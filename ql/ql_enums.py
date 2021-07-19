from pydantic import BaseModel, validator
from typing import List
from enum import Enum


class StartBasis(int, Enum):
    spot = 2
    tom = 1
    today = 0


class BusinessDay(str, Enum):
    no_adjustment = "No Adjustment" 
    following = "Following" 
    mod_following = "Modified Following"
    preceding = "Preceding"
    mod_preceding = "Modified Preceding"


class DayCount(str, Enum):
    act_365_fixed = 'Actual/365 Fixed' 
    act_365_fixed_canadian = 'Actual/365 Fixed (Canadian)'
    act_365_fixed_noleap = 'Actual/365 Fixed (No Leap)'
    act_360 = 'Actual/360'
    act_act = 'Actual/Actual'
    act_act_isma = 'Actual/Actual (ISMA)'
    act_act_bond = 'Actual/Actual (Bond)'
    act_act_isda = 'Actual/Actual (ISDA)'
    act_act_historical = 'Actual/Actual (Historical)'
    act_act_act365 ='Actual/Actual (Actual365)'
    act_act_afb = 'Actual/Actual (AFB)'
    business252 = 'Business252'
    thirty360 = 'Thirty360'


class DateGeneration(str, Enum):
    forward = "Forward from issue date"
    backward = "Backward from maturity date"
    zero = "Zero"
    third_wednesday = "ThirdWednesday"
    twentieth = "Twentieth"
    twentieth_IMM = "TwentiethIMM"
    cds = "CDS"
