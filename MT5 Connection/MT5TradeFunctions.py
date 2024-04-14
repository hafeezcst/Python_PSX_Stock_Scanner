# Load the MetaTrader5 package
import MetaTrader5 as mt5
import pandas as pd
import datetime as datetime
import datetime
from datetime import datetime, timedelta
import plotly.express as px

# initialize and login to MetaTrader5
if mt5.initialize():
    print("MT5 initialized")
# set the login details
login = 62668
password = 'Allah2meOnly!'
server = '4xCube-MT5'
# connect to the trade account using the specified login, password and server
mt5.login(login, password, server)

# get current symbol price
symbol_price = mt5.symbol_info_tick("EURUSDxx")._asdict()
print('symbol price', symbol_price)

# requesting tick data
tick_data = pd.DataFrame(mt5.copy_ticks_range("EURUSDxx", 
                                             datetime.now() - timedelta(hours=4), 
                                             datetime.now(), 
                                             mt5.COPY_TICKS_ALL))

fig = px.line(tick_data, x=tick_data['time'], y=[tick_data['bid'], tick_data['ask']])
# convert figure to GIF file
fig.write_gif('figure.gif')


# get the last tick
last_tick = mt5.symbol_info_tick("EURUSDxx")
print('last tick', last_tick)

# total number of orders
num_orders = mt5.orders_total()
print('total number of orders', num_orders) 

# list of orders
orders = mt5.orders_get()
print('list of orders', orders)

# total number of positions
num_positions = mt5.positions_total()
print('total number of positions', num_positions)

# list of positions
positions = mt5.positions_get()
print('list of positions', positions)

# number of history orders
# Calculate the start and end dates for the last one month
end_date = datetime.now()
start_date = end_date - timedelta(days=1)

num_order_history = mt5.history_orders_total(start_date, end_date)
print('number of history orders', num_order_history)

# list of history orders
order_history = mt5.history_orders_get(start_date, end_date)
print('list of history orders', order_history)

# number of history deals
num_deal_history = mt5.history_deals_total(start_date, end_date)
print('number of history deals', num_deal_history)

# number of history deals
deal_history = mt5.history_deals_get(start_date, end_date)
print('list of history deals', deal_history)