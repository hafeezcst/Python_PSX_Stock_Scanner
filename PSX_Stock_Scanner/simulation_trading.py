import pandas as pd

def simulate_trading(df_strong_buy, df_sell, df_all):
    portfolio = {}
    analysis_type = "D"  # Replace "YOUR_ANALYSIS_TYPE" with the actual analysis type
    cash = 10000000  # initial cash
    pnl = pd.DataFrame(columns=['Date and Time', 'Daily PnL', 'Weekly PnL', 'Monthly PnL'])
    for date in df_all['Date and Time'].unique():
        df_date = df_all[df_all['Date and Time'] == date]
        for symbol in df_strong_buy:
            row = df_date.loc[df_date['Symbol'] == symbol]
            if row.empty:
                continue
            price = row[f'{analysis_type} Close'].values[0]
            if symbol not in portfolio and cash >= price * 5:
                portfolio[symbol] = 5
                cash -= price * 5

        for symbol in df_sell:
            row = df_date.loc[df_date['Symbol'] == symbol]
            if row.empty or symbol not in portfolio:
                continue
            price = row[f'{analysis_type} Close'].values[0]
            cash += price * portfolio[symbol]
            del portfolio[symbol]

        # Calculate PnL
        daily_pnl = cash - 10000000  # Replace with actual calculation
        weekly_pnl = daily_pnl  # Replace with actual calculation
        monthly_pnl = daily_pnl  # Replace with actual calculation
        #pnl = pnl.append({'Date and Time': date, 'Daily PnL': daily_pnl, 'Weekly PnL': weekly_pnl, 'Monthly PnL': monthly_pnl}, ignore_index=True)
    # Write PnL to Excel
    pnl.to_excel('pnl.xlsx', index=False)

    return portfolio, cash