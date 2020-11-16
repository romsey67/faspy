import numba
from numpy import datetime64 as dt64
from .rmp_dates import day_count_factor as day_cf
from faspy.interestrate.rmp_curves import interpolation
import math


def bucketing(data, buckets, value_date, dfcurve=None, dfcurve_shifted=None):
    """
    Generate bonds coupon structures.

            Parameters:
                data: a list containing dictionary with the following keys - "id", "date" and "amount"
                buckets: a list containg dictionaries with the following keys - "from" and "to". The value for each key is number of days


            Returns:
                a dictionary with the following keys - date, dcf, time,
                days, df, rate
    """
    vdate = dt64(value_date,"D")
    mydata = list(data)
    calc_data = [{"days": _datediff(vdate, dt64(x["date"],"D")), "tenor": day_cf("Actual/365", vdate, dt64(x["date"],"D"))} for x in mydata]

    df_xaxis = [x["times"] for x in dfcurve]
    df_yaxis = [x["df"] for x in dfcurve]
    i_func = interpolation(df_xaxis,df_yaxis,1)
    df_array = [{"df": ifunc(x["tenor"])} for x in calc_data]

    dtlen = len(mydata)
    newdata=[]
    for i in range(dtlen):
        old = dict(mydata[i])
        new = dict(calc_data[i])
        df_dic = df_array[i]
        old.update(new)
        old.update(df_dic)
        newdata.append(old)
    return new_data

    mdur = [{"mod_duration": _mod_duration(float(x["amount"]),float(x["tenor"], float(x["df"])))} for x in new_data]

    for i in range(dtlen)
        old = new_data[i]
        new = mdur[i]
        old.update(new)

    return new_data
    

@numba.njit('float64(float64, float64)')
def _mod_duration(amount, time, df):
    crate = -math.log(df)/time
    value01 = amount * df
    df01 = math.exp(-time * (crate + 0.0001))
    value02 = amount * df01
    return (value02-value01) / 0.0001



@numba.njit('float64(float64, float64)')
def _cal_crate(time, df):
    crate = -math.log(df)/time
    return float(crate)

@numba.njit
def _datediff(date1, date2):
    return date2 - date1
