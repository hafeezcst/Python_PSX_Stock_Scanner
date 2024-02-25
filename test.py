import matplotlib.pyplot as plt

from tradingview_ta import TA_Handler, Interval, Exchange


Handler = TA_Handler(
    symbol="OGDC",
    screener="PAKISTAN",
    exchange="PSX",
    interval=Interval.INTERVAL_1_DAY,
)

indicator = Handler.get_analysis().indicators
movaverages= Handler.get_analysis().moving_averages
oscillators= Handler.get_analysis().oscillators
summary= Handler.get_analysis().summary

print(indicator)
print()
print(movaverages)
print()
print(oscillators)
print()
print(summary)
