import QuantLib as ql
from typing import List
from pymodels import *
from ql_utils import *
from ql_conventions import *


def rate_2_depohelpers(depo_setting: DepoSetting, rates: List[Rate],  calendar, ):
    depo_helpers = []
    business_day = ql_business_day[depo_setting.business_day]
    day_count = ql_day_count[depo_setting.day_count]
    for rate in rates:
        quote_handle = ql.QuoteHandle(ql.SimpleQuote(rate.rate/100))
        ql_period = ql.Period(rate.tenor)
        dr_helper = ql.DepositRateHelper(quote_handle, ql_period, 
                    depo_setting.start_basis, calendar, business_day,
                    depo_setting.eom, day_count)
        depo_helpers.append(dr_helper)
    
    return depo_helpers


def parrate_2_bondhelpers(rates: List[Rate], parbond_setting: BondSetting, calendar, ):
    depo_helpers = []
    business_day = ql_business_day[parbond_setting.business_day]
    day_count = ql_day_count[parbond_setting.day_count]
    for rate in rates:
        quote_handle = ql.QuoteHandle(ql.SimpleQuote(rate.rate/100))
        ql_period = ql.Period(rate.tenor)
        dr_helper = ql.DepositRateHelper(quote_handle, ql_period, 
                    depo_setting.start_basis, calendar, business_day,
                    depo_setting.eom, day_count)
        depo_helpers.append(dr_helper)


def depo_rate_2_helpers(value_date: str, depo_rates: List[Rate], holidays = List[Holiday] ):
    
    calc_date = datestr_to_qldate(value_date)
    ql.Settings.instance().evaluationDate = calc_date
    for depo_rate in depo_rates:
        quote = ql.QuoteHandle(ql.SimpleQuote(0.05))
        tenor = ql.Period(depo_rate.tenor)
        fixingDays = 2
        calendar = ql.TARGET()
        convention = ql.ModifiedFollowing
        endOfMonth = False
        dayCounter = ql.Actual360()
        ql.DepositRateHelper(quote, tenor, fixingDays, calendar, convention, endOfMonth, dayCounter)