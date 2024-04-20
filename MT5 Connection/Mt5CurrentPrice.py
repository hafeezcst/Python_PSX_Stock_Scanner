# Load the MetaTrader5 package
import MetaTrader5 as mt5
Path="C:\\Program Files\\MetaTrader 5\\terminal64.exe"

# initialize and login to MetaTrader5
def get_market_price(symbol, type):
    if type == mt5.ORDER_TYPE_BUY:
        return mt5.symbol_info(symbol).ask
    elif type == mt5.ORDER_TYPE_SELL:
        return mt5.symbol_info(symbol).bid


if mt5.initialize():
    print("MT5 initialized")
# set the login details
login = 167146561
password = 'Allah2meOnly!'
server = 'Exness-MT5Real3'
# connect to the trade account using the specified login, password and server
mt5.login(login, password, server, timeout=1000, portable_path=Path)


try:
    Price_Buy = get_market_price("XAUUSDm", mt5.ORDER_TYPE_BUY)
    #Price_Sell = get_market_price("XAUUSDm", mt5.ORDER_TYPE_SELL)

    print(Price_Buy)
    #print(Price_Sell)
except Exception as e:
    print("Error occurred:", str(e))
mt5.shutdown()
print("MT5 shut down")

        
        