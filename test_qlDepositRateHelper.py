
import QuantLib as ql


calc_date = ql.Date(15, 1, 2015)
ql.Settings.instance().evaluationDate = calc_date
quote = ql.QuoteHandle(ql.SimpleQuote(0.05))
tenor = ql.Period('1Y')
fixingDays = 2
calendar1 = ql.Singapore()
#calendar.
convention = ql.ModifiedFollowing
endOfMonth = False
dayCounter = ql.Actual360()
mdate = ql.DepositRateHelper(quote, tenor, fixingDays, calendar1, 
    convention, endOfMonth, dayCounter)

print(f"Maturity date form ql.DepositRateHelper: {mdate.maturityDate().ISO()}")
