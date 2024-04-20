# Load the MetaTrader5 package
import MetaTrader5 as mt5
import pandas as pd
# initialize and login to MetaTrader5
Path="C:\\Program Files\\MetaTrader 5\\terminal64.exe"
if mt5.initialize():
    print("MT5 initialized")
# set the login details
login = 167146561
password = 'Allah2meOnly!'
server = 'Exness-MT5Real3'
# connect to the trade account using the specified login, password and server
mt5.login(login, password, server, timeout=1000, portable_path=Path)
# get the account details
account = mt5.account_info()
#print(f"Account info {account}")
# get the account balance
balance = account.balance
print(f"account balance {balance}")
    
def get_market_price(symbol, type):
    if type == mt5.ORDER_TYPE_BUY:
        return mt5.symbol_info(symbol).ask
    elif type == mt5.ORDER_TYPE_SELL:
        return mt5.symbol_info(symbol).bid

Price_buy= get_market_price('XAUUSDm', mt5.ORDER_TYPE_BUY)
Price_sell= get_market_price('XAUUSDm', mt5.ORDER_TYPE_SELL)
print(Price_buy)
print(Price_sell)
mt5.shutdown()



        
        