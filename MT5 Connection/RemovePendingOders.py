# Load the MetaTrader5 package
import MetaTrader5 as mt5
import pandas as pd
# initialize and login to MetaTrader5
if mt5.initialize():
    print("MT5 initialized")
# set the login details
login = 62668
password = 'Allah2meOnly!'
server = '4xCube-MT5'
# connect to the trade account using the specified login, password and server
mt5.login(login, password, server)

# Remove Pending Order
pending_orders = mt5.orders_get()
print('open pending orders', pending_orders)

order1 = pending_orders[0]

request = {
    'action': mt5.TRADE_ACTION_REMOVE,
    'order': order1.ticket
}

mt5.order_send(request)
