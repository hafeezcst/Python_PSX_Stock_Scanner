import pandas as pd
import mplfinance as mpf
from tradingview_ta import TA_Handler, Interval

# Define the symbol and timeframe
symbol = "AAPL"
interval = Interval.INTERVAL_1_DAY  # You can choose other intervals like Interval.INTERVAL_1_HOUR

try:
    # Fetch the data from TradingView
    handler = TA_Handler()
    handler.set_symbol_as(symbol)
    handler.set_interval_as(interval)
    analysis = handler.get_analysis()

    # Extract the OHLCV data
    candles = analysis['indicators']['quote'][0]['candles']

    # Create a DataFrame for mplfinance
    df = pd.DataFrame(candles, columns=['timestamp', 'open', 'close', 'high', 'low', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')  # Convert timestamp to datetime

    # Plot the candlestick chart using mplfinance
    mpf.plot(df.set_index('timestamp'), type='candle', style='yahoo', volume=True)

except Exception as e:
    print(f"Error: {e}")
