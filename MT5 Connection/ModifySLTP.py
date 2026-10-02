import MetaTrader5 as mt5
import configparser

def modify_sl_tp(stop_loss, take_profit):
    # Load MT5 credentials from config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    login = int(config.get('mt5', 'login'))
    password = config.get('mt5', 'password')
    server = config.get('mt5', 'server')
    
    # initialize and login to MetaTrader5
    if mt5.initialize():
        print("MT5 initialized")

    # connect to the trade account using the specified login, password, and server
    mt5.login(login, password, server)

    # get all open positions
    positions = mt5.positions_get()
    print('open positions', positions)
    
    # iterate through each position and modify SL/TP
    for position in positions:
        request = {
            'action': mt5.TRADE_ACTION_SLTP,
            'position': position.ticket,
            'sl': stop_loss,
            'tp': take_profit
        }
        
        res = mt5.order_send(request)
        
        # check the execution result for each position
        if res.retcode != mt5.TRADE_RETCODE_DONE:
            print("order_send failed for position {}, retcode={}".format(position.ticket, res.retcode))
            # request the result as a dictionary and display it element by element
            result_dict = res._asdict()
            for field in result_dict.keys():
                print("   {}={}".format(field, result_dict[field]))
            if res.comment != "":
                print("   comment: {}".format(res.comment))

# Usage example
stop_loss = 100
take_profit = 200

modify_sl_tp(stop_loss, take_profit)
