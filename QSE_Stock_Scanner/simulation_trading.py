def simulate_trading(df_strong_buy, df_sell, df):
    portfolio = {}
    analysis_type = "D"  # Replace "YOUR_ANALYSIS_TYPE" with the actual analysis type
    cash = 100000  # initial cash
    for symbol in df_strong_buy:
        row = df.loc[df['Symbol'] == symbol]
        price = row[f'{analysis_type} Close'].values[0]
        if symbol not in portfolio and cash >= price * 1000:
            portfolio[symbol] = 1000
            cash -= price * 1000

    for symbol in df_sell:
        row = df.loc[df['Symbol'] == symbol]
        price = row[f'{analysis_type} Close'].values[0]
        if symbol in portfolio:
            cash += price * portfolio[symbol]
            del portfolio[symbol]

    return portfolio, cash