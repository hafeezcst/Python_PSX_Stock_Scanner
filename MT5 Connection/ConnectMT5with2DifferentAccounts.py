import MetaTrader5 as Mt5
from time import sleep
# display data on the MetaTrader 5 package
Path = "C:\Program Files\MetaTrader 5\terminal64.exe"
# establish connection to the MetaTrader 5 terminal
if not Mt5.initialize( ):
    print("initialize() failed, error code =", Mt5.last_error( ))
    quit()
 
# display data on MetaTrader 5 version
print( Mt5.version( ))
# connect to the trade account without specifying a password and a server
# Login to MetaTrader 5 terminal
Login4xc = 62668  # Replace with your actual login number
Password4xc = "Allah2meOnly!"  # Replace with your actual password
Server4xc = "4xCube-MT5"  # Replace with your actual server name

authorized = Mt5.login(login=Login4xc, password=Password4xc, server=Server4xc, path=Path)  # the terminal database password is applied if connection data is set to be remembered

# Display the path where the terminal connected
print("Terminal connected at path:", Path)
if authorized:
    # display trading account data 'as is'
    print( Mt5.account_info( ))
    # display trading account data in the form of a list
    print("Show account_info()._asdict():")
    account_info_dict = Mt5.account_info( )._asdict( )
    for prop in account_info_dict:
        print("  {}={}".format(prop, account_info_dict[prop]))
else:
    print("failed to connect at account #{}, error code: {}".format( Login4xc, Mt5.last_error( )))

sleep ( 10)
Mt5.shutdown()
print("disconnecting...4xcube done")
sleep ( 10)
if not Mt5.initialize( ):
    print("initialize() failed, error code =", Mt5.last_error( ))
    quit()
# now connect to another trading account specifying the password
# Login to MetaTrader 5 terminal
LoginPP = 51169531  # Replace with your actual login number
PasswordPP = "Allah2meOnly!"  # Replace with your actual password
ServerPP = "Pepperstone-MT5-Live01"  # Replace with your actual server name

authorized = Mt5.login( login=LoginPP, password=PasswordPP, server=ServerPP)
if authorized:
    # display trading account data 'as is'
    print( Mt5.account_info( ))
    # display trading account data in the form of a list
    print("Show account_info()._asdict():")
    account_info_dict = Mt5.account_info( )._asdict( )
    for prop in account_info_dict:
        print("  {}={}".format(prop, account_info_dict[prop]))
else:
    print("failed to connect at account #{}, error code: {}".format( LoginPP, Mt5.last_error( )))
 
# shut down connection to the MetaTrader 5 terminal
Mt5.shutdown()
print("disconnection pepperstone done")