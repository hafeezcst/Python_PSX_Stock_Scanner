# Load the MetaTrader5 package
import MetaTrader5 as mt5
import pandas as pd
import configparser

# Load MT5 credentials from config file
config = configparser.ConfigParser()
config.read('config.ini')

# initialize and login to MetaTrader5
Path = config.get('mt5', 'path', fallback="C:\\Program Files\\MetaTrader 5\\terminal64.exe")
if mt5.initialize():
    print("MT5 initialized")
# set the login details
login = int(config.get('mt5', 'login'))
password = config.get('mt5', 'password')
server = config.get('mt5', 'server')
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



        
        