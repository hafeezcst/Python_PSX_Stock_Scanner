
from tradingview_ta import TA_Handler, Interval, Exchange
OGDC = TA_Handler(
    symbol="OGDC",
    screener="PAKISTAN",
    exchange="PSX",
    interval=Interval.INTERVAL_1_DAY,
   
   )
print(OGDC.get_analysis().indicators)
print()
print(OGDC.get_analysis().oscillators)
print()
print(OGDC.get_analysis().moving_averages)
print()
print(OGDC.get_analysis().summary)
print()
print(OGDC.get_analysis().summary['BUY'])
print()
print(OGDC.get_analysis().summary,['RECOMENDATION'])