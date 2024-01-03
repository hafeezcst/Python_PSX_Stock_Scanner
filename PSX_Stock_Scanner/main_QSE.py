from convert_excel_to_lists import CUSTUM, KMIALL, KMI100, KMI30, MYLIST, QSE
from analysis_functions import analyze_symbol
from email_functions import send_email
from simulation_trading import simulate_trading
import time
import os
import logging
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import datetime
import sqlalchemy

# Configure logging
logging.basicConfig ( filename='analysis_log.txt', level=logging.ERROR )

def main():
    analysis_type = input (
        "Select analysis type (M for Monthly, W for Weekly, D for Daily,H for 4Hourly, press Enter for default D): " ).upper ( )
    
    if not analysis_type:
        time.sleep ( 2 )  # Delay for 5 seconds
        
        analysis_type = "D"  # Default selection
        print ( f"Selected analysis type: {analysis_type}" )
    
    if analysis_type not in [ "M", "W", "D", "H" ]:
        raise ValueError ( "Invalid analysis type. Please select M, W, D, or H" )
    
    recommendation_options = [ "STRONG_BUY", "BUY", "NEUTRAL", "SELL", "STRONG_SELL" ]
    
    recommendation_filter = input (
        f"Select recommendation filter ({', '.join ( recommendation_options )}): " ).upper ( )
    
    if not recommendation_filter:
        time.sleep ( 5 )  # Delay for 5 seconds
        recommendation_filter = "STRONG_BUY"  # Default selection
        print ( f"Selected recommendation filter: {recommendation_filter}" )
    while recommendation_filter not in recommendation_options :
        print ( "Invalid recommendation filter. Please try again." )
        recommendation_filter = input (
            f"Select recommendation filter ({', '.join ( recommendation_options )}): " ).upper ( )
    
    volume_threshold = 1000000  # Filter by this volume threshold 1 mission
    min_volume = 50000  # Filter by thids volume threshold
    ao_threshold: int = 0  # Filter by this AO threshold
    base_url_charts = "https://www.tradingview.com/chart/ZMYE714n/?symbol=PSX%3A"  # Set the base URL
    base_url_finance = "https://www.tradingview.com/symbols/PSX-"  # Set the base URL
    base_url_tech = "https://www.tradingview.com/symbols/PSX-"  # Set the base URL
    # Set default analysis type to "M" if the user presses Enter without entering a choice
    current_datetime = datetime.datetime.now ( )  # Include time
    count = 1
    
    # Create a thread pool
    with ThreadPoolExecutor ( max_workers=500 ) as executor :  # Adjust max_workers as needed
        # Submit tasks to the thread pool
        
        symbol_options = [ "KMIALL", "KMI100", "KMI30", "MYLIST", "QSE" ,"CUSTUM"]
        
        symbol_selection = input (
            f"Select symbol List ({', '.join ( symbol_options )}), press Enter for default List: " ).upper ( )
        
        if not symbol_selection:
            time.sleep ( 2 )  # Delay for 5 seconds
            symbol_selection = "KMI100"  # Default selection
            print ( f"Selected symbol List: {symbol_selection}" )
        while symbol_selection not in symbol_options :
            print ( "Invalid symbol selection. Please try again." )
            symbol_selection = input (
                f"Select symbol ({', '.join ( symbol_options )}), press Enter for default {symbol_selection} " ).upper ( )
        
        if symbol_selection == "KMI30":
            psx_symbols = KMI30
        elif symbol_selection == "KMI100":
            psx_symbols = KMI100
        elif symbol_selection == "MYLIST":
            psx_symbols = MYLIST
        elif symbol_selection == "CUSTUM": 
            psx_symbols = CUSTUM
        else :
            psx_symbols = KMIALL
        
        futures = [
            executor.submit ( analyze_symbol, symbol, analysis_type, base_url_charts, base_url_finance, base_url_tech )
            for symbol in psx_symbols ]
        
        # Process completed tasks
        analyzed_data = [ ]  # list to store all analyzed data
        strong_buy_symbols = [ ]  # List to store symbols with a "STRONG_BUY" recommendation
        buy_symbols = [ ]  # List to store symbols with a "BUY" recommendation
        sell_symbols = [ ]  # List to store symbols with a "SELL" recommendation

        for future in futures:
            result = future.result ( )
            if result:
                symbol, summary, Close, Sell_Signal, Neutral_Signal, Buy_Signal, Volume, ADX, RSI, RSI_Last, AO, Change,average_support, average_resistance, base_url_charts, base_url_finance, base_url_tech = result
                print ( f"{count}:  Symbol: {symbol}" )
                summary = (summary.get ( 'RECOMMENDATION' ))
                print ( summary )
                print (
                    f"{analysis_type} Sell_Signal:{Sell_Signal},Neutral_Signal:{Neutral_Signal},Buy_Signal:{Buy_Signal},CLOSE: {Close} Volume: {Volume} ADX:{ADX} RSI: {RSI} LAST RSI: {RSI_Last} AO: {AO} %Change(D): {Change} " )
                print ( )
                count += 1
                # Check if Volume and AO are not None before comparing
                if Volume is not None and AO is not None:
            # check and Append data to the list for CSV export if volume is greater than 5000
                    if Volume > min_volume :
                        analyzed_data.append([
                        current_datetime, symbol, summary, Close, Sell_Signal, Neutral_Signal, Buy_Signal, Volume,
                        ADX, RSI, RSI_Last, AO, Change,average_support,average_resistance, base_url_charts, base_url_finance, base_url_tech
                    ])
                
                # Check if the recommendation is "user defined" and the volume is greater than the threshold
                    if summary == recommendation_filter and Volume > volume_threshold and AO > ao_threshold :
                        strong_buy_symbols.append ([
                        current_datetime, symbol, summary, Close, Sell_Signal, Neutral_Signal, Buy_Signal, Volume,
                        ADX, RSI, RSI_Last, AO, Change,average_support,average_resistance, base_url_charts, base_url_finance, base_url_tech
                    ])
                # Check if the recommendation is "fixed buy" and the volume is greater than the threshold
                    if summary == "BUY" and Volume > volume_threshold and AO > ao_threshold :
                        buy_symbols.append ([
                        current_datetime, symbol, summary, Close, Sell_Signal, Neutral_Signal, Buy_Signal, Volume,
                        ADX, RSI, RSI_Last, AO, Change,average_support,average_resistance, base_url_charts, base_url_finance, base_url_tech
                    ])
                # Check if the recommendation is "fixed buy" and the volume is greater than the threshold
                    if summary == "SELL" and Volume > volume_threshold and AO < ao_threshold :
                        sell_symbols.append ([
                        current_datetime, symbol, summary, Close, Sell_Signal, Neutral_Signal, Buy_Signal, Volume,
                        ADX, RSI, RSI_Last, AO, Change,average_support,average_resistance, base_url_charts, base_url_finance, base_url_tech
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

        # Concatenate existing data with new data
        subset_columns = ['Symbol', 'Summary',f'{analysis_type} Close', 'Sell',
                            'Neutral', 'Buy', 'Volume', 'ADX', 'RSI',
                            'Last RSI', 'AO', '%Change(D)','Support','Resistance']
                            
        df_all = pd.concat ( [ df_all_symbols, pd.DataFrame ( analyzed_data,
                            columns=[ 'Date and Time', 'Symbol', 'Summary',
                            f'{analysis_type} Close', 'Sell',
                            'Neutral', 'Buy', 'Volume', 'ADX', 'RSI',
                            'Last RSI', 'AO', '%Change(D)','Support','Resistance',
                            'Charts', 'Financials', 'Technicals' ] ) ]).drop_duplicates ( ).drop_duplicates(subset=subset_columns,keep='last')  
        
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
                            'Financials', 'Technicals' ] ) ]
                            ).drop_duplicates(subset=subset_columns,keep='last')  
    else :
        # Create a new file
        subset_columns = ['Symbol', 'Summary',f'{analysis_type} Close', 'Sell',
                            'Neutral', 'Buy', 'Volume', 'ADX', 'RSI',
                            'Last RSI', 'AO', '%Change(D)','Support','Resistance']      
        df_all = pd.DataFrame ( analyzed_data,
                                columns=[ 'Date and Time', 'Symbol', 'Summary',
                            f'{analysis_type} Close', 'Sell',
                            'Neutral', 'Buy', 'Volume', 'ADX', 'RSI',
                            'Last RSI', 'AO', '%Change(D)','Support','Resistance',
                            'Charts', 'Financials', 'Technicals' ] ).drop_duplicates(subset=subset_columns,keep='last')   # Create a new DataFrame 
       
        df_strong_buy = pd.DataFrame ( strong_buy_symbols,
                                       columns=[ 'Date and Time', 'Symbol', 'Summary',
                            f'{analysis_type} Close', 'Sell',
                            'Neutral', 'Buy', 'Volume', 'ADX', 'RSI',
                            'Last RSI', 'AO', '%Change(D)','Support','Resistance',
                            'Charts', 'Financials', 'Technicals' ] ).drop_duplicates(subset=subset_columns,keep='last') 
        df_buy = pd.DataFrame ( buy_symbols,
                                columns=[ 'Date and Time', 'Symbol', 'Summary',
                            f'{analysis_type} Close', 'Sell',
                            'Neutral', 'Buy', 'Volume', 'ADX', 'RSI',
                            'Last RSI', 'AO', '%Change(D)','Support','Resistance',
                            'Charts', 'Financials', 'Technicals' ] ).drop_duplicates(subset=subset_columns,keep='last')  
        df_sell = pd.DataFrame ( sell_symbols,
                                columns=[ 'Date and Time', 'Symbol', 'Summary',
                            f'{analysis_type} Close', 'Sell',
                            'Neutral', 'Buy', 'Volume', 'ADX', 'RSI',
                            'Last RSI', 'AO', '%Change(D)','Support','Resistance',
                            'Charts', 'Financials', 'Technicals' ] ).drop_duplicates(subset=subset_columns,keep='last')  
    # Write the data to an Excel file
    
    # Define the database connection URL
    database_url = f'sqlite:///{analysis_type}_data.db'

    # Create a database engine
    engine = sqlalchemy.create_engine(database_url)

    # Write DataFrames to the database
    if df_all is not None or df_strong_buy is not None or df_buy is not None or df_sell is not None:
        df_all.to_sql('all_symbols', engine, if_exists='append', index=False)
        df_strong_buy.to_sql('recommended_symbols', engine, if_exists='append', index=False)
        df_buy.to_sql('buy_symbols', engine, if_exists='append', index=False)
        df_sell.to_sql('sell_symbols', engine, if_exists='append', index=False)
    else:
        print("df_all is None")
    

    # Save the Excel file
    with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
        # Write DataFrames to Excel sheets
        df_all.to_excel(writer, sheet_name='All Symbols', index=False)
        df_strong_buy.to_excel(writer, sheet_name='Recommended_Symbols', index=False)
        df_buy.to_excel(writer, sheet_name='Buy_Symbols', index=False)
        df_sell.to_excel(writer, sheet_name='Sell_Symbols', index=False)

        # Get the workbook and the worksheet objects
        workbook = writer.book
        worksheet_all = writer.sheets [ 'All Symbols' ]
        worksheet_strong_buy = writer.sheets [ 'Recommended_Symbols' ]
        worksheet_buy = writer.sheets [ 'Buy_Symbols' ]
        worksheet_sell = writer.sheets [ 'Sell_Symbols' ]
        # Set the column width and format
        # Define the format for highlighting
        highlight_format_bullish = workbook.add_format ( {'bg_color' : '#75AA74'} )
        highlight_format_bearish = workbook.add_format ( {'bg_color' : '#FFC7CE'} )
        # Set the column width and format

        # Apply conditional formatting to the 'All Symbols' sheet
        worksheet_all.conditional_format ( 'A2:Q1000', {'type' : 'formula',
                                                        'criteria' : 'AND($K2>50, $L2>0)',
                                                        'format' : highlight_format_bullish} )
        
        # Apply conditional formatting to the '{recommendation_filter}_Symbols' sheet
        worksheet_strong_buy.conditional_format ( 'A2:Q1000', {'type' : 'formula',
                                                               'criteria' : 'AND($K2>50, $L2>0)',
                                                               'format' : highlight_format_bullish} )
        # Apply conditional formatting to the '{recommendation_filter}_Symbols' sheet
        worksheet_buy.conditional_format ( 'A2:Q1000', {'type' : 'formula',
                                                        'criteria' : 'AND($K2>50, $L2>0)',
                                                        'format' : highlight_format_bullish} )
        # Apply conditional formatting to the '{recommendation_filter}_Symbols' sheet
        worksheet_sell.conditional_format ( 'A2:Q1000', {'type' : 'formula',
                                                        'criteria' : 'AND($K2<50, $L2<0)',
                                                        'format' : highlight_format_bearish} )
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
        # Explicitly close the Excel writer
        writer.close ( )
        
        # Add a short delay (e.g., 1 second) before sending the email
        time.sleep ( 3 )
        # send email
        # Assuming the correct DataFrame is named df_strong_buy:
        recommended_symbols = df_strong_buy
        buy_symbols = df_buy
        # Filter the symbols for the current date
        # Filter the symbols for the current date
        today_Strong_buy = recommended_symbols [
            recommended_symbols [ 'Date and Time' ].dt.date == datetime.datetime.now ( ).date ( ) ]
        today_buy = buy_symbols [
            buy_symbols [ 'Date and Time' ].dt.date == datetime.datetime.now ( ).date ( ) ]
        # Sort the data by recommendation 
        subject = f"{analysis_type}-{symbol_selection}- {recommendation_filter}-Technical_Analysis_"
        # body    = f"Technical Analysis for {current_date} is attached."
        # Concatenate the two DataFrames
        combined_df = pd.concat ( [ today_Strong_buy, today_buy ] )
        # Convert the concatenated DataFrame to a string
        body = combined_df.to_string ( index=False )
        attachment_path = excel_file_path
        send_email ( subject, body, attachment_path )
        # Sort the Excel file by symbol and date and time
        # Open the file using the default program associated with Excel files
        os.system ( f'start excel.exe "{excel_file_path}"' )
        # Wait for 5 seconds before running the analysis again
        time.sleep ( 5 )  # Adjust the delay as needed

if __name__ == "__main__":
    analyzed_data = [ ]  # Moved analyzed_data outside the loop to persist data across runs
    strong_buy_symbols = [ ]  # Moved strong_buy_symbols outside the loop to persist data across runs
    buy_symbols = [ ]  # Moved buy_symbols outside the loop to persist data across runs
    
    # Call the simulate_trading function

    # Run the main analysis
    main ( )
