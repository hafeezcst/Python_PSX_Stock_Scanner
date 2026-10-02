import MetaTrader5 as Mt5
import configparser

# Load MT5 credentials from config file
config = configparser.ConfigParser()
config.read('config.ini')

# Login to MetaTrader 5 terminal
Login = int(config.get('mt5', 'login'))
Password = config.get('mt5', 'password')
Server = config.get('mt5', 'server')
Path = config.get('mt5', 'path', fallback="C:\\Program Files\\MetaTrader 5\\terminal64.exe")
# establish MetaTrader 5 connection to a specified trading account
if not Mt5.initialize ( login=Login, server=Server, password=Password, path=Path):
    print ( "initialize() failed, error code =", Mt5.last_error ( ))
    quit ( )

# display data on connection status, server name and trading account
print ( "Successfully connected to PepperStone MT5")
# print(mt5.terminal_info())
# display data on MetaTrader 5 version
print ( Mt5.version ( ))
# display data on the MetaTrader 5 package
print ( "MetaTrader5 package author: ", Mt5.__author__)
print ( "MetaTrader5 package version: ", Mt5.__version__)
# shut down connection to the MetaTrader 5 terminal
Mt5.shutdown ( )
print ( "Successfully Disconnected to PepperStone MT5")
