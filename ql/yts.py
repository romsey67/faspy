from typing import List
from pymodels import *
import QuantLib as ql
from ql.pym_ql_utils import *

from ql.ql_utils import *


def calc_curve(value_date: str, depo_setting: DepoSetting, depo_rates: List[Rate], 
    par_setting:BondSetting, par_rates: List[Rate], holidays: List[Holiday]=[], ccy="MYR"):

    
    vdate = datestr_to_qldate(value_date)
    depo_helpers = rate_2_depohelpers(depo_setting, depo_rates,)
    ql.Settings.instance().evaluationDate = vdate






