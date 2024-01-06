symbol = "AAPL"  # Replace "AAPL" with the desired symbol

from tradingview_ta import TA_Handler, Interval

analysis = TA_Handler(symbol="OGDC", screener="PAKISTAN", exchange="PSX",
                      interval=Interval.INTERVAL_1_MONTH)

analysis = analysis.get_analysis()

print(analysis.moving_averages['RECOMMENDATION'])
compute=(analysis.oscillators['COMPUTE'])
for i in compute:
    print(i)
print(compute[i])


print(analysis.oscillators['RECOMMENDATION'])
print(analysis.indicators['RSI'])
print(analysis.summary["RECOMMENDATION"])

