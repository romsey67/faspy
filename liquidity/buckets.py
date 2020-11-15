import numba
from numpy import datetime64 as dt64
from faspy.interestrate.rmp_dates import day_count_factor as day_cf


def bucketing(data, buckets, value_date, df=None, df_shifted=None):
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
    new_data = [x.update({"days": _datediff(vdate, dt64(x["date"],"D")), "tenor": day_cf("Actual/365", vdate, dt64(x["date"],"D"))}) for x in data]

    return new_data



@numba.njit
def _datediff(date1, date2):
    return date2 - date1
