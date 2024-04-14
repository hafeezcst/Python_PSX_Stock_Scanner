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

# connect to the trade account using the specified login, password and server
mt5.login(login, password, server)
    
def get_market_price(symbol, type):
    if type == mt5.ORDER_TYPE_BUY:
        return mt5.symbol_info(symbol).ask
    elif type == mt5.ORDER_TYPE_SELL:
        return mt5.symbol_info(symbol).bid

get_market_price('XAUUSDx', mt5.ORDER_TYPE_BUY)
get_market_price('XAUUSDx', mt5.ORDER_TYPE_SELL)
prices = pd.DataFrame(columns=['symbol', 'buy', 'sell'])
prices = prices.append({'symbol': 'XAUUSD', 'buy': get_market_price('XAUUSD', mt5.ORDER_TYPE_BUY), 'sell': get_market_price('XAUUSD', mt5.ORDER_TYPE_SELL)}, ignore_index=True)
print(prices)
mt5.shutdown()
print("MT5 shut down")

        
        