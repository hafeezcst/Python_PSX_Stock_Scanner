import time
def get_symbol_selection():
    symbol_options = ["KMIALL", "KMI100", "KMI30", "MYLIST", "QSE", "CUSTUM"]
    
    symbol_selection = input(f"Select symbol List ({', '.join(symbol_options)}), press Enter for default List KMIALL or QSE: ").upper()
    
    if not symbol_selection:
        time.sleep(2)
        symbol_selection = "KMIALL"
        print(f"Selected symbol List: {symbol_selection}")

    while symbol_selection not in symbol_options:
        print("Invalid symbol selection. Please try again.")
        symbol_selection = input(f"Select symbol ({', '.join(symbol_options)}), press Enter for default {symbol_selection}: ").upper()

    return symbol_selection