# Load the MetaTrader5 package
import MetaTrader5 as mt5
# initialize and login to MetaTrader5
def get_market_price(symbol, type):
    if type == mt5.ORDER_TYPE_BUY:
        return mt5.symbol_info(symbol).ask
    elif type == mt5.ORDER_TYPE_SELL:
        return mt5.symbol_info(symbol).bid

login = 10001900739
password = 'RxVt*fk7'
server = 'MetaQuotes-Demo'

if mt5.initialize():
    print("MT5 initialized")
# set the login details
# connect to the trade account using the specified login, password and server
mt5.login(login, password, server)

try:
    Price = get_market_price("XAUUSD", mt5.ORDER_TYPE_BUY)
    print(Price)
except Exception as e:
    print("Error occurred:", str(e))
mt5.shutdown()
print("MT5 shut down")

        
        