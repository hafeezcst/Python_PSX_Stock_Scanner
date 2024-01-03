from email import encoders
from email.mime.base import MIMEBase
import os
from threading import Thread
import datetime
from concurrent.futures import ThreadPoolExecutor
import openpyxl
from tradingview_ta import TA_Handler, Interval
import pandas as pd
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
# Configure logging
logging.basicConfig(filename='analysis_log.txt', level=logging.ERROR)
# Load the Workbook
cwd = os.getcwd()
excel_file = os.path.join(cwd, 'PSXSymbols.xlsx')
wb = openpyxl.load_workbook(excel_file)

# Initialize empty lists for data
KMIALL, KMI100, KMI30, MYLIST, QSE= [], [], [], [],[]

# Loop through each sheet
for sheet_name in ("KMIALL", "KMI100", "KMI30", "MYLIST","QSE"):
    sheet = wb[sheet_name]

    # Assuming data starts at row 2 and column 1 (adjust if needed)
    for row in sheet.iter_rows(min_row=2):
        symbol = row[0].value  # Assuming symbols are in the first column

        # Append symbol to corresponding list
        if sheet_name == "KMIALL":
            KMIALL.append(symbol)
        elif sheet_name == "KMI100":
            KMI100.append(symbol)
        elif sheet_name == "KMI30":
            KMI30.append(symbol)
        elif sheet_name == "MYLIST":
            MYLIST.append(symbol)
        elif sheet_name == "QSE":
            QSE.append(symbol)

# Print the extracted lists for confirmation
#print(f"KMIALL: {KMIALL}")
#print(f"KMI100: {KMI100}")
#print(f"KMI30: {KMI30}")
#print(f"MYLIST: {MYLIST}")
#print(f"QSE: {QSE}")
# (Optional) Close the workbook
wb.close()

def analyze_symbol(symbol, analysis_type, base_url_charts, base_url_finance, base_url_tech):
    """

    :param base_url_finance:
    :param symbol:
    :param analysis_type:
    :param base_url_charts:
    :param base_url_tech:
    :return:
    """
    try:
        if analysis_type == "M":
            analysis     = TA_Handler ( symbol=symbol, screener="PAKISTAN", exchange="PSX",
                                    interval=Interval.INTERVAL_1_MONTH )
        elif analysis_type == "W":
            analysis     = TA_Handler ( symbol=symbol, screener="PAKISTAN", exchange="PSX",
                                    interval=Interval.INTERVAL_1_WEEK )
        elif analysis_type == "D":
            analysis     = TA_Handler ( symbol=symbol, screener="PAKISTAN", exchange="PSX",
                                    interval=Interval.INTERVAL_1_DAY )
        elif analysis_type == "4H":
            analysis     = TA_Handler ( symbol=symbol, screener="PAKISTAN", exchange="PSX",
                                    interval=Interval.INTERVAL_4_HOURS )

        if 'analysis' in locals ( ) and analysis is not None and analysis.get_analysis ( ) is not None:
            summary            = analysis.get_analysis().summary
            indicators         = analysis.get_analysis().indicators
            oscillator         = analysis.get_analysis().oscillators
            moving_averages    = analysis.get_analysis().moving_averages

            if summary is not None:
                buy_signal      = summary['BUY']
                sell_signal     = summary['SELL']
                neutral_signal  = summary['NEUTRAL']
                rsi             = indicators['RSI']
                rsi_last        = indicators['RSI[1]']
                close           = indicators['close']
                volume          = indicators['volume']
                ao              = indicators['AO']
                change          = indicators['change']
                adx             = indicators['ADX']

                # Construct the website link
                charts = f"{base_url_charts}{symbol}"
                financials = f"{base_url_finance}{symbol}/financials-overview/"
                technicals = f"{base_url_tech}{symbol}/technicals/"

                return symbol, summary, close, sell_signal, neutral_signal, buy_signal, volume, adx, rsi, rsi_last, ao, change, charts, financials, technicals

    except Exception as e:
        error_message = f"Exception occurred for symbol: {symbol}. Error Message: {e}"
        logging.error(f"{datetime.datetime.now()} - {error_message}")
        print(error_message)
    return None

def send_email(subject, body, attachment_path=None):
    """

    :param subject:
    :param body:
    :param attachment_path:
    """
    # Email configuration
    sender_email = "hafeezcst@gmail.com"  # Replace with your email address
    receiver_emails = ["hafeezcst@gmail.com","tahir_inspection@yahoo.com","ammarhafeez3495@gmail.com","amok3495@gmail.com"]  # Replace with the recipient's email addresses
    # receiver_email = ", ".join(receiver_emails)
    smtp_server = "smtp.gmail.com"  # Replace with your SMTP server (e.g., smtp.gmail.com for Gmail)
    smtp_port = 587  # Replace with your SMTP port (587 is the default for TLS)

    # Email account credentials
    username = "hafeezcst@gmail.com"  # Replace with your email address
    # Update this line with your application-specific password
    password = "ujdw djtr anws chry"

    # Create the email message
    message = MIMEMultipart ( )
    message["From"] = sender_email
    message["To"] = ", ".join ( receiver_emails )
    message["Subject"] = subject
    message.attach ( MIMEText ( body, "plain" ) )

    if attachment_path:
        with open ( attachment_path, "rb" ) as attachment:
            part = MIMEBase ( "application", "octet-stream" )
            part.set_payload ( attachment.read ( ) )
        encoders.encode_base64 ( part )
        part.add_header (
            "Content-Disposition",
            f"attachment; filename= {os.path.basename ( attachment_path )}",
        )
        message.attach ( part )

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP ( smtp_server, smtp_port )
        server.starttls ( )
        server.login ( username, password )

        # Send the email
        server.sendmail ( sender_email, receiver_emails, message.as_string ( ) )
        print ( "Email sent successfully" )

    except Exception as e:
        error_message = f"Error sending email: {e}"
        logging.error(f"{datetime.datetime.now()} - {error_message}")
        print(error_message)
    finally:
        # Disconnect from the SMTP server
        server.quit ( )


def run_analysis_daily():
    while True:
        current_datetime = datetime.datetime.now ( )
        print ( f"Technical Analysis Date and Time: {current_datetime}" )

        analyzed_data.clear ( )

        # Calculate the time difference until the next day
        next_day = current_datetime + datetime.timedelta ( days=1 )
        time_difference = next_day.replace ( hour=7, minute=00, second=0, microsecond=0 ) - current_datetime
        print ( f"Time until the next day: {time_difference}" )

        # Sleep for the calculated time difference
        time.sleep ( time_difference.total_seconds ( ) )

        # Filter symbols with a "STRONG_BUY" recommendation
        strong_buy_symbols = [data for data in analyzed_data if data[2] == "STRONG_BUY"]

        # Send email if there are strong buy symbols

        if strong_buy_symbols:
            subject = "Daily Strong Buy Recommendations"
            body = "\n".join ( [f"{symbol}: {recommendation}" for _, symbol, recommendation, *_ in strong_buy_symbols] )

            send_email ( subject, body )

            # Sleep for 24 hours- 86400 seconds
        time.sleep ( 86400 )

def main():
    
    recommendation_filter = "BUY" # Default selection
    print(recommendation_filter)
    volume_threshold = 1000000  # Filter by this volume threshold 1 misslion
    ao_threshold: int   = 0  # Filter by this AO threshold
    base_url_charts     = "https://www.tradingview.com/chart/ZMYE714n/?symbol=PSX%3A"  # Set the base URL
    base_url_finance    = "https://www.tradingview.com/symbols/PSX-"  # Set the base URL
    base_url_tech       = "https://www.tradingview.com/symbols/PSX-"  # Set the base URL
    # Set default analysis type to "M" if the user presses Enter without entering a choice
    analysis_type = "4H"
    print(analysis_type)
    current_datetime = datetime.datetime.now ( ).strftime("%m:%d:%Y %H:%M:%S")  # Include time
    print ( f"Technical Analysis Date and Time: {current_datetime}" )
    count = 1
    # Create a thread pool
    with ThreadPoolExecutor ( max_workers=500 ) as executor:  # Adjust max_workers as needed
        # Submit tasks to the thread pool
        symbol_options = ["KMIALL", "KMI100", "KMI30", "MYLIST", "QSE"]
        symbol_selection = "KMI100"  # Default selection
        print(symbol_selection)

        if symbol_selection == "KMI30":
            psx_symbols = KMI30
        elif symbol_selection == "KMI100":
            psx_symbols = KMI100
        elif symbol_selection == "MYLIST":
            psx_symbols = MYLIST
        elif symbol_selection == "QSE":
            psx_symbols = QSE
        else:
            psx_symbols = KMIALL

        futures = [
            executor.submit ( analyze_symbol, symbol, analysis_type, base_url_charts, base_url_finance, base_url_tech )
            for symbol in psx_symbols]

        # Process completed tasks
        analyzed_data = []
        strong_buy_symbols = []  # List to store symbols with a "STRONG_BUY" recommendation
        strong_buy_calculations = []  # List to store symbols with a "STRONG_BUY" recommendation
        for future in futures:
            result = future.result ( )
            if result:
                symbol, summary, Close, Sell_Signal, Neutral_Signal, Buy_Signal, Volume, ADX, RSI, RSI_Last, AO, Change, base_url_charts, base_url_finance, base_url_tech = result
                print ( f"{count}:  Symbol: {symbol}" )
                summary = (summary.get ( 'RECOMMENDATION' ))
                print ( summary )
                print (
                    f"{analysis_type} Sell_Signal:{Sell_Signal},Neutral_Signal:{Neutral_Signal},Buy_Signal:{Buy_Signal},CLOSE: {Close} Volume: {Volume} ADX:{ADX} RSI: {RSI} LAST RSI: {RSI_Last} AO: {AO} %Change(D): {Change} " )
                print ( )
                count += 1

                # check and Append data to the list for CSV export if volme is greater than 5000
                if Volume > 0:
                    analyzed_data.append (
                        [current_datetime, symbol, summary, Close, Sell_Signal, Neutral_Signal, Buy_Signal, Volume, ADX,
                         RSI, RSI_Last, AO, Change, base_url_charts, base_url_finance, base_url_tech] )

                # Check if the recommendation is "user defined" and the volume is greater than the threshold
                if summary == recommendation_filter and Volume > volume_threshold:
                    strong_buy_symbols.append (
                        [current_datetime, symbol, summary, Close, Sell_Signal, Neutral_Signal, Buy_Signal, Volume, ADX,
                         RSI, RSI_Last, AO, Change, base_url_charts, base_url_finance, base_url_tech] )     
       
        # Get the current date
        current_date = datetime.datetime.now ( ).strftime ( "%Y%m" )
        # Set the file name with the analysis date as a postfix
        excel_file_path = f"{analysis_type}-Advance_Technical_Analysis_{symbol_selection}_{recommendation_filter}.xlsx"
        # Specify the sheet names you want to read
        sheet_names = ['All Symbols', 'Recomended_Symbols']
    # Check if the file exists
    if os.path.exists(excel_file_path):
    # Read existing data from the file
        # Read data from each sheet into separate DataFrames
        df_all_symbols = pd.read_excel(excel_file_path, sheet_name='All Symbols')
        df_strong_buy_symbols = pd.read_excel(excel_file_path, sheet_name='Recomended_Symbols')
    # Concatenate existing data with new data
        df_all = pd.concat([df_all_symbols, pd.DataFrame(analyzed_data, columns=['Date and Time', 'Symbol', 'Summary', f'{analysis_type} Close', 'Sell',
                                                                      'Neutral', 'Buy', 'Volume', 'ADX', 'RSI', 'Last RSI', 'AO', '%Change(D)',
                                                                      'Charts', 'Financials', 'Technicals'])], ignore_index=True).drop_duplicates()

        df_strong_buy = pd.concat([df_strong_buy_symbols, pd.DataFrame(strong_buy_symbols, columns=['Date and Time', 'Symbol', 'Summary', f'{analysis_type} Close',
                                                                                  'Sell','Neutral', 'Buy', 'Volume', 'ADX', 'RSI', 'Last RSI', 'AO',
                                                                                  '%Change(D)', 'Charts', 'Financials', 'Technicals'])], ignore_index=True).drop_duplicates()
    else:
    # Create a new file
        df_all = pd.DataFrame(analyzed_data, columns=['Date and Time', 'Symbol', 'Summary', f'{analysis_type} Close', 'Sell',
                                                    'Neutral', 'Buy', 'Volume', 'ADX', 'RSI', 'Last RSI', 'AO', '%Change(D)',
                                                  'Charts', 'Financials', 'Technicals'])

        df_strong_buy = pd.DataFrame(strong_buy_symbols, columns=['Date and Time', 'Symbol', 'Summary', f'{analysis_type} Close',
                                                              'Sell','Neutral', 'Buy', 'Volume', 'ADX', 'RSI', 'Last RSI', 'AO',
                                                              '%Change(D)', 'Charts', 'Financials', 'Technicals'])

    with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
            # Write DataFrames to Excel sheets
        df_all.to_excel ( writer, sheet_name='All Symbols', index=False )
        df_strong_buy.to_excel ( writer, sheet_name='Recomended_Symbols', index=False )

            # Get the workbook and the worksheet objects
        workbook = writer.book
        worksheet_all = writer.sheets['All Symbols']
        worksheet_strong_buy = writer.sheets['Recomended_Symbols']
            # New sheet for P&L analysis
            # Define the format for highlighting
        highlight_format = workbook.add_format ( {'bg_color': '#00AA00'} )

            # Apply conditional formatting to the 'All Symbols' sheet
        worksheet_all.conditional_format ( 'A2:Q1000', {'type': 'formula',
                                                            'criteria': 'AND($J2>50, $l2>0)',
                                                            'format': highlight_format} )

            # Apply conditional formatting to the '{recommendation_filter}_Symbols' sheet
        worksheet_strong_buy.conditional_format ( 'A2:Q1000', {'type': 'formula',
                                                                   'criteria': 'AND($J2>50, $l2>0)',
                                                                   'format': highlight_format} )
        print ( f"Data exported to {excel_file_path}" )
        
        # Wait until the file size stabilizes (e.g., for 5 seconds)
        initial_size = os.path.getsize(excel_file_path)
        time.sleep(5)  # Adjust the delay as needed
    while True:
        current_size = os.path.getsize(excel_file_path)
        if current_size == initial_size:
            break  # File size has stabilized
        initial_size = current_size
        time.sleep(2)  # Wait and check again
       # Explicitly close the Excel writer
        writer.close()

        # send email
        # Assuming the correct DataFrame is named df_strong_buy:
        recommended_symbols = df_strong_buy
        todays_data = recommended_symbols[recommended_symbols['Date and Time'] == datetime.datetime.now ( ).strftime ( "%m/%d/%Y" )]
        subject = f"{analysis_type}-{symbol_selection}- {recommendation_filter}-Technical_Analysis_"
        # body    = f"Technical Analysis for {current_date} is attached."
        body = todays_data.to_string ( )
        attachment_path = excel_file_path
        send_email ( subject, body, attachment_path )
        # Sort the Excel file by symbol and date and time
        # Open the file using the default program associated with Excel files
        #os.system ( f'start excel.exe "{excel_file_path}"' )

if __name__ == "__main__":
    analyzed_data = []  # Moved analyzed_data outside the loop to persist data across runs
    # Schedule the daily analysis to run continuously
    Thread ( target=run_analysis_daily, daemon=True ).start ( )

    # Run the main analysis
    main ( )

