import MetaTrader5 as Mt5

# Login to MetaTrader 5 terminal
Login = 62668  # Replace with your actual login number
Password = "Allah2meOnly!"  # Replace with your actual password
Server = "4xCube-MT5"  # Replace with your actual server name

Path = Path = "C:/Program Files/4xCube MT5 Terminal/terminal64.exe"

# establish MetaTrader 5 connection to a specified trading account
if not Mt5.initialize ( login=Login, server=Server, password=Password ):
    print ( "initialize() failed, error code =", Mt5.last_error ( ) )
    quit ( )

# display data on connection status, server name and trading account
print ( "Successfully connected to 4xCube MT5")
# print(mt5.terminal_info())
# display data on MetaTrader 5 version

# display data on the MetaTrader 5 package
print ( "MetaTrader5 package author: ", Mt5.__author__ )
print ( "MetaTrader5 package version: ", Mt5.__version__ )
print ( Mt5.version ( ) )

# shut down connection to the MetaTrader 5 terminal
Mt5.shutdown ( )
print ( "Successfully Disconnected to 4xCube MT5")
