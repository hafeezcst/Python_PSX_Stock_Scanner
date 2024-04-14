
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


# close position

positions = mt5.positions_get()
print('open positions', positions)

# Working with 1st position in the list and closing it
pos1 = positions[0]

def reverse_type(type):
    # to close a buy positions, you must perform a sell position and vice versa
    if type == mt5.ORDER_TYPE_BUY:
        return mt5.ORDER_TYPE_SELL
    elif type == mt5.ORDER_TYPE_SELL:
        return mt5.ORDER_TYPE_BUY


def get_close_price(symbol, type):
    if type == mt5.ORDER_TYPE_BUY:
        return mt5.symbol_info(symbol).bid
    elif type == mt5.ORDER_TYPE_SELL:
        return mt5.symbol_info(symbol).ask

request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "position": pos1.ticket,
    "symbol": pos1.symbol,
    "volume": pos1.volume,
    "type": reverse_type(pos1.type),
    "price":get_close_price(pos1.symbol, pos1.type),
    "deviation": 20,
    "magic": 0,
    "comment": "python close order",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,  # some brokers accept mt5.ORDER_FILLING_FOK only
}

res = mt5.order_send(request)
# check the execution result
if res.retcode != mt5.TRADE_RETCODE_DONE:
    print("order_send failed, retcode={}".format(res.retcode))
    # request the result as a dictionary and display it element by element
    result_dict = res._asdict()
    for field in result_dict.keys():
        print("   {}={}".format(field, result_dict[field]))
    if res.comment != "":
        print("   comment: {}".format(res.comment))