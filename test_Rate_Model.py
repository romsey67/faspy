from ql.ql_utils import create_calendar
from ql.pymodels import *
import QuantLib as ql

rates = [{"tenor": "1M", "rate": 4.00}, 
        {"tenor": "3M", "rate": 4.10}, 
        {"tenor": "6M", "rate": 4.20}]

for therate in rates:
    rate = Rate(**therate)




theset = {"start_basis": 5}
trs = DepoSetting(**theset)
print(trs.start_basis)
trs.start_basis = 5
print(trs.start_basis)



