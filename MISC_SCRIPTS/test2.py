import pandas as pd
import  os

df = pd.read_excel('C:\\Users\\Administrator\\Documents\\GitHub\\Python_PSX_Stock_Scanner\\D-Advance_Technical_Analysis_QSE_STRONG_BUY.xlsx')
print(df.columns)
# Extract the date and time components
df['Date and Time'] = pd.to_datetime(df['Date and Time'], format='%H:%M:%Y')
df['Date and Time'] = df['Date and Time'].dt.date


# Save the modified DataFrame back to the Excel file
df.to_excel('C:\\Users\\Administrator\\Documents\\GitHub\\Python_PSX_Stock_Scanner\\D-Advance_Technical_Analysis_QSE_STRONG_BUY.xlsx', index=False)