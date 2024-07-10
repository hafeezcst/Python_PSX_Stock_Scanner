from stockchartview import capture_stock_charts
import pandas as pd

def get_symbol_selection():
    df = pd.read_excel('psxsymbols.xlsx', sheet_name='KMI100')
    symbol_selection = df.iloc[:, 0].tolist()
    return symbol_selection
symbol_selection = get_symbol_selection()
for symbol in symbol_selection:
    capture_stock_charts(symbol)  # Replace "OGDC" with any symbol you want to capture
    print(f"Chart for {symbol} has been captured")

print("All charts have been captured")