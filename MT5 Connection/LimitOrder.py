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


# limit orders

symbol = 'EURUSDxx'
volume = 0.01

action = mt5.TRADE_ACTION_PENDING
order_type = mt5.ORDER_TYPE_BUY_LIMIT
limit_price = 1.0

stop_loss = 0.9  # set to 0.0 if you don't want SL
take_profit = 1.2  # set to 0.0 if you don't want TP

request = {
    "action": action,
    "symbol": 'EURUSDxx',
    "volume": 0.1,  # float
    "type": order_type,
    "price": limit_price,
    "sl": stop_loss,  # float
    "tp": take_profit,  # float
    "deviation": 20,
    "magic": 0,
    "comment": "python market order",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,  # some brokers accept mt5.ORDER_FILLING_FOK only
}

res = mt5.order_send(request)
print('order send result', res)
# check the execution result
if res.retcode != mt5.TRADE_RETCODE_DONE:
    print("order_send failed, retcode={}".format(res.retcode))
    # request the result as a dictionary and display it element by element
    result_dict = res._asdict()
    for field in result_dict.keys():
        print("   {}={}".format(field, result_dict[field]))
    if res.comment != "":
        print("   comment: ", res.comment)