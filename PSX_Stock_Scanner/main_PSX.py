from convert_excel_to_lists import CUSTUM, KMIALL, KMI100, KMI30, MYLIST, QSE
from analysis_functions import analyze_symbol
from openpyxl.styles import PatternFill
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.formatting.rule import Rule
from email_functions import send_email
import pandas as pd
import sqlalchemy
import time
import os
import logging
import datetime
from concurrent.futures import ThreadPoolExecutor
# Set up logging
logging.basicConfig(filename='analysis_log.txt', level=logging.ERROR)

# Global constants
# Set the volume threshold to 1,000,000
VOLUME_THRESHOLD = 1000000

# Set the minimum volume to 50,000
MIN_VOLUME = 50000

# Set the AO threshold to 0
AO_THRESHOLD = 0

# Configure logging
logging.basicConfig ( filename='analysis_log.txt', level=logging.ERROR )

def main():
    # Ask the user to select the analysis type and convert the input to uppercase
    analysis_type = input(
        "Select analysis type (M for Monthly, W for Weekly, D for Daily,H for Hourly, press Enter for default D): "
    ).upper()
    # If the user didn't provide any input
    if not analysis_type:
        # Wait for 2 seconds
        time.sleep(2)
        # Set the analysis type to "D" by default
        analysis_type = "D"
        # Print the selected analysis type
        print(f"Selected analysis type: {analysis_type}")

     # Ask the user to select the analysis type and convert the input to uppercase
    country_selection = input("Select analysis type (P for Pakistan, Q for Qatar, press Enter for default PAKISTAN):").upper()
    # If the user didn't provide any input
    if country_selection=="P":
        # Wait for 2 seconds
        time.sleep(2)
        # Set the analysis type to "D" by default
        screener_selection,exchange_selection = "PAKISTAN","PSX"
        BASE_URL_CHARTS = f"https://www.tradingview.com/chart/ZMYE714n/?symbol=PSX%3A"
        BASE_URL_FINANCE = f"https://www.tradingview.com/symbols/PSX-"
        BASE_URL_TECH = f"https://www.tradingview.com/symbols/PSX-"
        # Print the selected analysis type
        print(f"Selected country : {screener_selection}")
        print(f"Selected exchange: {exchange_selection}")
    elif country_selection=="Q":
        # Wait for 2 seconds
        time.sleep(2)
        # Set the analysis type to "D" by default
        screener_selection,exchange_selection = "QATAR","QSE"
        BASE_URL_CHARTS = f"https://www.tradingview.com/chart/ZMYE714n/?symbol=QSE%3A"
        BASE_URL_FINANCE = f"https://www.tradingview.com/symbols/QSE-"
        BASE_URL_TECH = f"https://www.tradingview.com/symbols/QSE-"
        # Print the selected analysis type
        print(f"Selected country : {screener_selection}")
        print(f"Selected exchange: {exchange_selection}")


    # If the analysis type is not valid
    if analysis_type not in ["M", "W", "D", "H"]:
        # Raise a ValueError with a message
        raise ValueError("Invalid analysis type. Please select M, W, D, or H")

    # Define the recommendation options
    recommendation_options = ["STRONG_BUY", "BUY", "NEUTRAL", "SELL", "STRONG_SELL"]

    # Ask the user to select a recommendation filter and convert the input to uppercase
    recommendation_filter = input(
        f"Select recommendation filter ({', '.join(recommendation_options)}): "
    ).upper()

    # If the user didn't provide any input
    if not recommendation_filter:
        # Wait for 5 seconds
        time.sleep(5)
        
        # Set the recommendation filter to "STRONG_BUY" by default
        recommendation_filter = "STRONG_BUY"
        
        # Print the selected recommendation filter
        print(f"Selected recommendation filter: {recommendation_filter}")

    # While the recommendation filter is not valid
    while recommendation_filter not in recommendation_options:
        # Print a message
        print("Invalid recommendation filter. Please try again.")
        
        # Ask the user to select a recommendation filter again
        recommendation_filter = input(
            f"Select recommendation filter ({', '.join(recommendation_options)}): "
        ).upper()

    # Set default analysis type to "M" if the user presses Enter without entering a choice
    current_datetime = datetime.datetime.now ( )  # Include time
    count = 1
    
    # Create a thread pool
    with ThreadPoolExecutor ( max_workers=500 ) as executor :  # Adjust max_workers as needed
        # Submit tasks to the thread pool
        
        symbol_options = [ "KMIALL", "KMI100", "KMI30", "MYLIST", "QSE" ,"CUSTUM"]
        
        symbol_selection = input (
            f"Select symbol List ({', '.join ( symbol_options )}), press Enter for default List KMIALL: " ).upper ( )
        
        if not symbol_selection and country_selection=="P":
            time.sleep ( 2 )  # Delay for 5 seconds
            symbol_selection = "KMIALL"  # Default selection
            print ( f"Selected symbol List: {symbol_selection}" )
        elif not symbol_selection and country_selection=="Q":
            time.sleep ( 2 )
            symbol_selection = "QSE"  # Default selection
            print ( f"Selected symbol List: {symbol_selection}" )
        # While the symbol_selection is not valid
        while symbol_selection not in symbol_options :
            print ( "Invalid symbol selection. Please try again." )
            symbol_selection = input (
                f"Select symbol ({', '.join ( symbol_options )}), press Enter for default{symbol_selection}: " ).upper ( )
        
        # If symbol_selection is "KMI30"
        if symbol_selection == "KMI30":
            # Set psx_symbols to the value of KMI30
            psx_symbols = KMI30
        # Else, if symbol_selection is "KMI100"
        elif symbol_selection == "KMI100":
            # Set psx_symbols to the value of KMI100
            psx_symbols = KMI100
        # Else, if symbol_selection is "MYLIST"
        elif symbol_selection == "MYLIST":
            # Set psx_symbols to the value of MYLIST
            psx_symbols = MYLIST
        # Else, if symbol_selection is "CUSTUM"
        elif symbol_selection == "CUSTUM":
            # Set psx_symbols to the value of CUSTUM
            psx_symbols = CUSTUM
        elif symbol_selection == "QSE":
            # Set psx_symbols to the value of CUSTUM
            psx_symbols = QSE
        # Else, if symbol_selection is anything else
        else:
            # Set psx_symbols to the value of KMIALL
            psx_symbols = KMIALL
        # Define the base URLs        

        # For each symbol in psx_symbols
        futures = [
            # Submit a task to the executor to analyze the symbol
            executor.submit(
                analyze_symbol,  # The function to execute
                symbol,  # The symbol to analyze
                analysis_type,  # The type of analysis to perform
                screener_selection,  # The screener to use
                exchange_selection,  # The exchange to use
                BASE_URL_CHARTS,  # The base URL for chart data
                BASE_URL_FINANCE,  # The base URL for financial data
                BASE_URL_TECH  # The base URL for technical data
            )
            for symbol in psx_symbols  # The list of symbols to analyze
        ]
        
        # Initialize an empty list to store all analyzed data
        analyzed_data = []

        # Initialize an empty list to store symbols with a "STRONG_BUY" recommendation
        strong_buy_symbols = []

        # Initialize an empty list to store symbols with a "BUY" recommendation
        buy_symbols = []

        # Initialize an empty list to store symbols with a "SELL" recommendation
        sell_symbols = []
        # For each future in the list of futures
        for future in futures:
            # Get the result of the future
            result = future.result()

            # If the result is not None
            if result:
                # Unpack the result into multiple variables
                symbol, summary, Close, Sell_Signal, Neutral_Signal, Buy_Signal, Volume, ADX, RSI, RSI_Last, AO, Change,average_support, average_resistance, BASE_URL_CHARTS, BASE_URL_FINANCE, BASE_URL_TECH = result

                # Print the count and symbol
                print(f"{count}:  Symbol: {symbol}")

                # Get the 'RECOMMENDATION' from the summary
                summary = summary.get('RECOMMENDATION')

                # Print the summary
                print(summary)

                # Print various details about the symbol
                print(f"{analysis_type} Sell_Signal:{Sell_Signal},Neutral_Signal:{Neutral_Signal},Buy_Signal:{Buy_Signal},CLOSE: {Close} Volume: {Volume} ADX:{ADX} RSI: {RSI} LAST RSI: {RSI_Last} AO: {AO} %Change(D): {Change}")

                # Print an empty line
                print()

                # Increment the count
                count += 1

                # If Volume and AO are not None
                if symbol in ["ALLSHR", "KSE30", "KSE100","GNRI"] or (Volume is not None and AO is not None):
                    # If Volume is greater than min_volume
                    if symbol in ["ALLSHR", "KSE30", "KSE100","GNRI"] or Volume > MIN_VOLUME:
                        # Append the result to the analyzed_data list
                        analyzed_data.append([
                            current_datetime, symbol, summary, Close, Sell_Signal, Neutral_Signal, Buy_Signal, Volume,
                            ADX, RSI, RSI_Last, AO, Change,average_support,average_resistance, BASE_URL_CHARTS, BASE_URL_FINANCE, BASE_URL_TECH
                        ])
                
                # Check if the recommendation is "user defined" and the volume is greater than the threshold
                    if symbol in ["ALLSHR", "KSE30", "KSE100","GNRI"] or (summary == recommendation_filter and Volume > VOLUME_THRESHOLD and AO > AO_THRESHOLD) :
                        strong_buy_symbols.append ([
                        current_datetime, symbol, summary, Close, Sell_Signal, Neutral_Signal, Buy_Signal, Volume,
                        ADX, RSI, RSI_Last, AO, Change,average_support,average_resistance, BASE_URL_CHARTS, BASE_URL_FINANCE, BASE_URL_TECH
                    ])
                        
                # Check if the recommendation is "fixed buy" and the volume is greater than the threshold
                    if symbol in ["ALLSHR", "KSE30", "KSE100","GNRI"] or (summary == "BUY" and Volume>MIN_VOLUME and AO > AO_THRESHOLD) :
                        buy_symbols.append ([
                        current_datetime, symbol, summary, Close, Sell_Signal, Neutral_Signal, Buy_Signal, Volume,
                        ADX, RSI, RSI_Last, AO, Change,average_support,average_resistance, BASE_URL_CHARTS, BASE_URL_FINANCE, BASE_URL_TECH
                    ])
                # Check if the recommendation is "fixed buy" and the volume is greater than the threshold
                    if summary == "SELL"  and AO < AO_THRESHOLD :
                        sell_symbols.append ([
                        current_datetime, symbol, summary, Close, Sell_Signal, Neutral_Signal, Buy_Signal, Volume,
                        ADX, RSI, RSI_Last, AO, Change,average_support,average_resistance, BASE_URL_CHARTS, BASE_URL_FINANCE, BASE_URL_TECH
                    ])
                else:
                    print("Volume or AO is None, skipping comparison")
                
        # Set the file name with the analysis date as a postfix
        excel_file_path = f"{analysis_type}-Advance_Technical_Analysis_{symbol_selection}_{recommendation_filter}.xlsx"
    # Check if the file exists
    if os.path.exists ( excel_file_path ) :
        print ( f"Reading data from {excel_file_path}" )
        # Read existing data from the file
        # Read data from each sheet into separate DataFrames 
        while True:
            try:
                df_all_symbols = pd.read_excel ( excel_file_path, sheet_name='All Symbols' )
                df_strong_buy_symbols = pd.read_excel ( excel_file_path, sheet_name='Recommended_Symbols' )
                df_buy_symbols = pd.read_excel ( excel_file_path, sheet_name='Buy_Symbols' )
                df_sell_symbols = pd.read_excel ( excel_file_path, sheet_name='Sell_Symbols' )
                break  # If the file opens successfully, break the loop
            except PermissionError:
                print(f"Waiting for file to close: {excel_file_path}")
                time.sleep(5)  # Wait for 5 seconds before trying again            

        # Define a list of column names
        subset_columns = [
            'Symbol',  # The symbol of the stock
            'Summary',  # The summary of the analysis
            f'{analysis_type} Close',  # The closing price, with the analysis type as a prefix
            'Sell',  # The sell signal
            'Neutral',  # The neutral signal
            'Buy',  # The buy signal
            'Volume',  # The trading volume
            'ADX',  # The Average Directional Index
            'RSI',  # The Relative Strength Index
            'Last RSI',  # The last value of the Relative Strength Index
            'AO',  # The Awesome Oscillator
            '%Change(D)',  # The daily percentage change
            'Support',  # The support level
            'Resistance'  # The resistance level
        ]
                            
        df_all = pd.concat ( [ df_all_symbols, pd.DataFrame ( analyzed_data,
                            columns=[ 'Date and Time', 'Symbol', 'Summary',
                            f'{analysis_type} Close', 'Sell',
                            'Neutral', 'Buy', 'Volume', 'ADX', 'RSI',
                            'Last RSI', 'AO', '%Change(D)','Support','Resistance',
                            'Charts', 'Financials', 'Technicals' ] ) ]).drop_duplicates(subset=subset_columns,keep='last')
        
        df_strong_buy = pd.concat ( [ df_strong_buy_symbols, pd.DataFrame ( strong_buy_symbols,
                            columns=[ 'Date and Time', 'Symbol', 'Summary',
                            f'{analysis_type} Close', 'Sell',
                            'Neutral', 'Buy', 'Volume', 'ADX', 'RSI',
                            'Last RSI', 'AO', '%Change(D)','Support','Resistance',
                            'Charts', 'Financials', 'Technicals' ] ) ] ).drop_duplicates(subset=subset_columns,keep='last')
        
        df_buy = pd.concat ( [ df_buy_symbols, pd.DataFrame ( buy_symbols,
                            columns=[ 'Date and Time', 'Symbol',
                            'Summary',
                            f'{analysis_type} Close',
                            'Sell', 'Neutral', 'Buy',
                            'Volume', 'ADX', 'RSI',
                            'Last RSI', 'AO',
                            '%Change(D)','Support','Resistance', 'Charts',
                            'Financials', 'Technicals' ] )]).drop_duplicates(subset=subset_columns,keep='last')
        df_sell = pd.concat ( [ df_sell_symbols, pd.DataFrame ( sell_symbols,
                            columns=[ 'Date and Time', 'Symbol',
                            'Summary',
                            f'{analysis_type} Close',
                            'Sell', 'Neutral', 'Buy',
                            'Volume', 'ADX', 'RSI',
                            'Last RSI', 'AO',
                            '%Change(D)','Support','Resistance', 'Charts',
                            'Financials', 'Technicals' ] ) ]).drop_duplicates(subset=subset_columns,keep='last')
    else :
        # Create a new file
        subset_columns = ['Symbol', 'Summary',f'{analysis_type} Close', 'Sell',
                            'Neutral', 'Buy', 'Volume', 'ADX', 'RSI',
                            'Last RSI', 'AO', '%Change(D)','Support','Resistance']      
        df_all = pd.DataFrame ( analyzed_data,
                                columns=[ 'Date and Time', 'Symbol', 'Summary',
                            f'{analysis_type} Close', 'Sell','Neutral', 'Buy', 'Volume', 'ADX', 'RSI',
                            'Last RSI', 'AO', '%Change(D)','Support','Resistance',
                            'Charts', 'Financials', 'Technicals' ] )
       
        df_strong_buy = pd.DataFrame ( strong_buy_symbols,
                                       columns=[ 'Date and Time', 'Symbol', 'Summary',
                            f'{analysis_type} Close', 'Sell',
                            'Neutral', 'Buy', 'Volume', 'ADX', 'RSI',
                            'Last RSI', 'AO', '%Change(D)','Support','Resistance',
                            'Charts', 'Financials', 'Technicals' ] )
        df_buy = pd.DataFrame ( buy_symbols,
                                columns=[ 'Date and Time', 'Symbol', 'Summary',
                            f'{analysis_type} Close', 'Sell',
                            'Neutral', 'Buy', 'Volume', 'ADX', 'RSI',
                            'Last RSI', 'AO', '%Change(D)','Support','Resistance',
                            'Charts', 'Financials', 'Technicals' ] )
        df_sell = pd.DataFrame ( sell_symbols,
                                columns=[ 'Date and Time', 'Symbol', 'Summary',
                            f'{analysis_type} Close', 'Sell',
                            'Neutral', 'Buy', 'Volume', 'ADX', 'RSI',
                            'Last RSI', 'AO', '%Change(D)','Support','Resistance',
                            'Charts', 'Financials', 'Technicals' ] )

    
    # Define the database connection URL
    # The URL is in the format 'sqlite:///<database_name>.db'
    # The database name is a combination of the symbol_selection and analysis_type variables
    database_url = f'sqlite:///{symbol_selection}_{analysis_type}_data.db'

    # Create a database engine
    # The engine is an instance of a SQLAlchemy Engine, which is the starting point for any SQLAlchemy application
    # It's the home base for the actual database and its DBAPI, delivered to the SQLAlchemy application through a connection pool and a Dialect
    engine = sqlalchemy.create_engine(database_url)

    # Write DataFrames to the database
    # If at least one of the DataFrames is not None
    if df_all is not None or df_strong_buy is not None or df_buy is not None or df_sell is not None:
        # Write df_all to a SQL table named 'all_symbols'
        df_all.to_sql('all_symbols', engine, if_exists='append', index=False)
        # Write df_strong_buy to a SQL table named 'recommended_symbols'
        df_strong_buy.to_sql('recommended_symbols', engine, if_exists='append', index=False)
        # Write df_buy to a SQL table named 'buy_symbols'
        df_buy.to_sql('buy_symbols', engine, if_exists='append', index=False)
        # Write df_sell to a SQL table named 'sell_symbols'
        df_sell.to_sql('sell_symbols', engine, if_exists='append', index=False)
    else:
        # If all the DataFrames are None, print a message
        print("df_all is None")

    # Save the Excel file
    with pd.ExcelWriter(excel_file_path, engine='openpyxl',mode='a',if_sheet_exists='replace') as writer:
        # Write df_all to an Excel sheet named 'All Symbols', without the index
        df_all.to_excel(writer, sheet_name='All Symbols', index=False)

        # Write df_strong_buy to an Excel sheet named 'Recommended_Symbols', without the index
        df_strong_buy.to_excel(writer, sheet_name='Recommended_Symbols', index=False)

        # Write df_buy to an Excel sheet named 'Buy_Symbols', without the index
        df_buy.to_excel(writer, sheet_name='Buy_Symbols', index=False)

        # Write df_sell to an Excel sheet named 'Sell_Symbols', without the index
        df_sell.to_excel(writer, sheet_name='Sell_Symbols', index=False)
        

        # Get the worksheet named 'All Symbols'
        worksheet_all = writer.sheets['All Symbols']
        
        # Get the worksheet named 'Recommended_Symbols'
        worksheet_strong_buy = writer.sheets['Recommended_Symbols']

        # Get the worksheet named 'Buy_Symbols'
        worksheet_buy = writer.sheets['Buy_Symbols']

        # Get the worksheet named 'Sell_Symbols'
        worksheet_sell = writer.sheets['Sell_Symbols']
        # Set the column width and format
        # Define the format for highlighting
 
        # Create a fill pattern
        highlight_format_bullish = PatternFill(start_color="75AA74", end_color="75AA74", fill_type="solid")
        # Create a fill pattern
        highlight_format_bearish = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
 
        # Create a differential style
        dxf_bullish = DifferentialStyle(fill=highlight_format_bullish)
        dxf_bearish = DifferentialStyle(fill=highlight_format_bearish)

        # Create a rule bullish
        rule_bullish = Rule(type="expression", dxf=dxf_bullish)
        rule_bullish.formula = ["$J1>50"]and ["$L1>0"]
        # Create a rule bearish
        rule_bearish = Rule(type="expression", dxf=dxf_bearish)
        rule_bearish.formula = ["$J1<50"] and ["$L1<0"]
     
        # Add the rule to the worksheet
        worksheet_all.conditional_formatting.add("A1:R1000", rule_bullish)
        worksheet_strong_buy.conditional_formatting.add("A1:R1000", rule_bullish)
        worksheet_buy.conditional_formatting.add("A1:R1000", rule_bullish)
        worksheet_sell.conditional_formatting.add("A1:R1000", rule_bearish)
        # Save the Excel file
        print ( f"Data exported to {excel_file_path}" )
        # Wait until the file size stabilizes (e.g., for 5 seconds)
        initial_size = os.path.getsize ( excel_file_path )
        time.sleep ( 5 )  # Adjust the delay as needed
    while True :
        current_size = os.path.getsize ( excel_file_path )
        if current_size == initial_size :
            break  # File size has stabilized
        initial_size = current_size
        time.sleep ( 2 )  # Wait and check again
        # Explicitly close the Excel write
        # Add a short delay (e.g., 1 second) before sending the email
        time.sleep ( 3 )

        # send email
        # Assuming the correct DataFrame is named df_strong_buy:
        # Sort df_strong_buy by 'Date and Time' in descending order
        recommended_symbols = df_strong_buy.sort_values(by='Date and Time', ascending=False)

        # Sort df_buy by 'Date and Time' in descending order
        buy_symbols = df_buy.sort_values(by='Date and Time', ascending=False)
        # Filter the symbols for the current date
        # Filter the symbols for the current date
        today_date          = datetime.datetime.now().date()
        today_Strong_buy    = recommended_symbols[recommended_symbols['Date and Time'].dt.date == today_date] if not recommended_symbols.empty else pd.DataFrame()
        today_buy           = buy_symbols[buy_symbols['Date and Time'].dt.date == today_date] if not buy_symbols.empty else pd.DataFrame()
        # Sort the data by recommendation 
        subject = f"{analysis_type}-{symbol_selection}- {recommendation_filter}-Technical_Analysis_"
        # body    = f"Technical Analysis for {current_date} is attached."
        # body    = f"Technical Analysis for {current_date} is attached."
        # Concatenate the two DataFrames
        combined_df = pd.concat([today_Strong_buy, today_buy])
        # Convert the concatenated DataFrame to a string
        body = combined_df.to_string ( index=False ,justify='left',col_space=10,header=True,na_rep='NaN',formatters=None,sparsify=None)
        attachment_path = excel_file_path
        send_email ( subject, body, attachment_path )
        # Sort the Excel file by symbol and date and time
        # Open the file using the default program associated with Excel files
        os.system ( f'start excel.exe "{excel_file_path}"' )
        # Wait for 5 seconds before running the analysis again
        time.sleep ( 5 )  # Adjust the delay as needed

# If this script is the main module (i.e., it's not being imported by another script)
if __name__ == "__main__":
    # Initialize an empty list to store all analyzed data
    analyzed_data = []

    # Initialize an empty list to store symbols with a "STRONG_BUY" recommendation
    strong_buy_symbols = []

    # Initialize an empty list to store symbols with a "BUY" recommendation
    buy_symbols = []

    # Call the main function to run the main analysis
    main()