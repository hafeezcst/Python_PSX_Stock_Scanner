# Load the MetaTrader5 package
import MetaTrader5 as mt5
import pandas as pd

def send_market_order(symbol, volume, order_type, stop_loss, take_profit):
    # initialize and login to MetaTrader5
    if mt5.initialize():
        print("MT5 initialized")
    
    # set the login details
    login = 62668
    password = 'Allah2meOnly!'
    server = '4xCube-MT5'
    
    # connect to the trade account using the specified login, password and server
    mt5.login(login, password, server)
    
    def get_market_price(symbol, type):
        if type == mt5.ORDER_TYPE_BUY:
            return mt5.symbol_info(symbol).ask
        elif type == mt5.ORDER_TYPE_SELL:
            return mt5.symbol_info(symbol).bid
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": get_market_price(symbol, order_type),
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": 20,
        "magic": 0,
        "comment": "python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
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

# Usage example
symbol = "EURUSD"
volume = 0.01
order_type = mt5.ORDER_TYPE_BUY
stop_loss = 1.0
take_profit = 2.0

send_market_order(symbol, volume, order_type, stop_loss, take_profit)