
import mplfinance as mpf
import yfinance as yf

# Get Tesla stock data from Yahoo Finance
tesla = yf.download('TSLA')

# Create a new figure and plot the chart
fig, ax = mpf.plot(tesla, type='candle', savefig='chart.png')

# Save the figure as a PNG file
fig.savefig('chart.png')
