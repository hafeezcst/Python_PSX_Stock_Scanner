

import matplotlib.pyplot as plt

from tradingview_ta import TA_Handler, Interval, Exchange
import pandas as pd

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

countS = 0
countR = 0
psumS = 0  # Initialize psumS variable
psumR = 0  # Initialize psumR variable
pivot_values_S = []  # List to store pivot values for support
pivot_values_R = []  # List to store pivot values for resistance
searchtext1 = "pivot" # support value - if x.lower().startswith("pivot") and x[:-1].lower().endswith("s"):
searchtext2 = "s" # resistance value - if x.lower().startswith("pivot") and x[:-1].lower().endswith("r"):
searchtext3 = "r" # resistance value - if x.lower().startswith("pivot") and x[:-1].lower().endswith("r"):

for x in indicator: 
    if x.lower().startswith(searchtext1) and x[:-1].lower().endswith(searchtext2):
        countS += 1
        pivotvalue = Handler.get_analysis().indicators[x]
        psumS += pivotvalue  # Accumulate pivotvalue for calculating average
        pivot_values_S.append(pivotvalue)
        print(countS, '-', x, ':', pivotvalue)

print(f'Support: {psumS/countS}')

for x in indicator:
    if x.lower().startswith(searchtext1) and x[:-1].lower().endswith(searchtext3):
        countR += 1
        pivotvalue = Handler.get_analysis().indicators[x]
        psumR += pivotvalue  # Accumulate pivotvalue for calculating average
        pivot_values_R.append(pivotvalue)
        print(countR, '-', x, ':', pivotvalue)

print(f'Resistance {psumR/countR}')

for ind in oscillators:
    print (f'oscillator:{ind}', Handler.get_analysis())

import matplotlib.pyplot as plt

# Plotting trend chart for support pivot values
fig, (ax1, ax2) = plt.subplots(2, 1)

ax1.plot(range(len(pivot_values_S)), pivot_values_S)
ax1.axhline(y=psumS/countS, color='r', linestyle='--')  # Add horizontal line for average
ax1.text(0, psumS/countS, f'Average: {psumS/countS}', color='r')  # Add text for average value
ax1.set_xlabel('Support Pivot')
ax1.set_ylabel('Pivot Value')
ax1.set_title('Support Pivot Values')

# Plotting trend chart for resistance pivot values
ax2.plot(range(len(pivot_values_R)), pivot_values_R)
ax2.axhline(y=psumR/countR, color='r', linestyle='--')  # Add horizontal line for average

ax2.set_xlabel('Resistance Pivot')
ax2.set_ylabel('Pivot Value')
ax2.set_title('Resistance Pivot Values')

# Add average value to the plot
ax2.axhline(y=psumR/countR, color='r', linestyle='--')  # Add horizontal line for average
ax2.text(0, psumR/countR, f'Average: {psumR/countR}', color='r')  # Add text for average value

plt.tight_layout()
plt.show()

# Export charts to Excel
df_support = pd.DataFrame({'Support Pivot': pivot_values_S})
df_resistance = pd.DataFrame({'Resistance Pivot': pivot_values_R})

with pd.ExcelWriter('pivot_charts.xlsx') as writer:
    df_support.to_excel(writer, sheet_name='Support Pivot Chart', index=False)
    df_resistance.to_excel(writer, sheet_name='Resistance Pivot Chart', index=False)

# Plotting trend chart for support pivot values
fig, (ax1, ax2) = plt.subplots(2, 1)

ax1.plot(range(len(pivot_values_S)), pivot_values_S)
ax1.axhline(y=psumS/countS, color='r', linestyle='--')  # Add horizontal line for average
ax1.text(0, psumS/countS, f'Average: {psumS/countS}', color='r')  # Add text for average value
ax1.set_xlabel('Support Pivot')
ax1.set_ylabel('Pivot Value')
ax1.set_title('Support Pivot Values')

# Plotting trend chart for resistance pivot values
ax2.plot(range(len(pivot_values_R)), pivot_values_R)
ax2.axhline(y=psumR/countR, color='r', linestyle='--')  # Add horizontal line for average
ax2.text(0, psumR/countR, f'Average: {psumR/countR}', color='r')  # Add text for average value
ax2.set_xlabel('Resistance Pivot')
ax2.set_ylabel('Pivot Value')
ax2.set_title('Resistance Pivot Values')

plt.tight_layout()
plt.savefig('pivot_charts.png')
plt.close()




