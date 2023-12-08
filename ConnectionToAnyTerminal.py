import MetaTrader5 as mt5
from tabulate import tabulate
import os
import csv

# Specify the terminal paths
terminal_paths = [
    "C:\\Program Files\\MetaTrader 5\\terminal64.exe",
    "C:\\Program Files\\4xCube MT5 Terminal\\terminal64.exe",
    "C:\\Program Files\\Pepperstone MetaTrader 5\\terminal64.exe",
    "C:\\Program Files\\MetaTrader 5 EXNESS\\terminal64.exe"
]

# Check if any of the terminal paths exist
valid_terminal_path = None
for i, terminal_path in enumerate(terminal_paths):
    if os.path.exists(terminal_path):
        print(f"{i+1}. {terminal_path}")
valid_terminal_index = int(input("Select a valid terminal path: ")) - 1
valid_terminal_path = terminal_paths[valid_terminal_index] if 0 <= valid_terminal_index < len(terminal_paths) else None

# Connect to the MetaTrader 5 terminal
if valid_terminal_path is not None:
    if not mt5.initialize(valid_terminal_path):
        print("Failed to initialize MetaTrader 5 terminal, error code =", mt5.last_error())
        quit()
else:
    print(" Valid MetaTrader 5 terminal found at the specified paths.")
    quit()

# Get all symbols
symbols = mt5.symbols_get()
# Create a list of symbol names
symbol_names = [s.name for s in symbols]
# Create a table with the symbol names
table_data = [[i+1, name] for i, name in enumerate(symbol_names)]
table_headers = ["No.", "Symbol Name"]
table = tabulate(table_data, headers=table_headers, tablefmt="grid")

# Display the table
print(table)

# ... (existing code)

# Create a list of symbol names and their indices
symbol_data = [[i+1, name] for i, name in enumerate(symbol_names)]

# Export the symbol data to a CSV file
csv_file = "symbol_data.csv"
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["No.", "Symbol Name"])  # Write the header
    writer.writerows(symbol_data)  # Write the symbol data

print(f"Symbol data exported to {csv_file}")

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()

# Get symbols containing RU in their names
ru_symbols = mt5.symbols_get("*RU*")
if ru_symbols is not None:
    print('len(*RU*): ', len(ru_symbols))
    for s in ru_symbols:
        print(s.name)
    print()
else:
    print('No symbols found containing RU in their names.')
 
# get symbols whose names do not contain USD, EUR, JPY and GBP
group_symbols = mt5.symbols_get(group="*,!*USD*,!*EUR*,!*JPY*,!*GBP*")
if group_symbols is not None:
    print('len(*,!*USD*,!*EUR*,!*JPY*,!*GBP*):', len(group_symbols))
    for s in group_symbols:
        print(s.name, ":", s)
else:
    print('No symbols found whose names do not contain USD, EUR, JPY and GBP.')
 
# shut down connection to the MetaTrader 5 terminal
Disconnection = mt5.shutdown()
if Disconnection:
    print("Successfully Disconnected from")

# Connect to the MetaTrader 5 terminal
if valid_terminal_path is not None:
    if not mt5.initialize(valid_terminal_path):
        print("Failed to initialize MetaTrader 5 terminal, error code =", mt5.last_error())
        quit()
else:
    print("No valid MetaTrader 5 terminal found at the specified paths.")
    quit()

# Get all symbols
symbols = mt5.symbols_get()
# Create a list of symbol names
symbol_names = [s.name for s in symbols]
# Create a table with the symbol names
table_data = [[i+1, name] for i, name in enumerate(symbol_names)]
table_headers = ["No.", "Symbol Name"]
table = tabulate(table_data, headers=table_headers, tablefmt="grid")

# Display the table
print(table)

# Shut down connection to the MetaTrader 5 terminal
mt5.shutdown()

# Get symbols containing RU in their names
ru_symbols = mt5.symbols_get("*RU*")
if ru_symbols is not None:
    print('len(*RU*): ', len(ru_symbols))
    for s in ru_symbols:
        print(s.name)
    print()
else:
    print('No symbols found containing RU in their names.')
 
# get symbols whose names do not contain USD, EUR, JPY and GBP
group_symbols = mt5.symbols_get(group="*,!*USD*,!*EUR*,!*JPY*,!*GBP*")
if group_symbols is not None:
    print('len(*,!*USD*,!*EUR*,!*JPY*,!*GBP*):', len(group_symbols))
    for s in group_symbols:
        print(s.name, ":", s)
else:
    print('No symbols found whose names do not contain USD, EUR, JPY and GBP.')

# Shut down connection to the MetaTrader 5 terminal
Disconnection = mt5.shutdown()
if Disconnection:
    print("Successfully Disconnected from", valid_terminal_path)
    