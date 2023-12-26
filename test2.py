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
KMIALL, KMI100, KMI30, MYLIST, QSE = [], [], [], [], []

# Loop through each sheet
for sheet_name in ("KMIALL", "KMI100", "KMI30", "MYLIST", "QSE"):
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

# Close the workbook
wb.close()

def analyze_symbol(symbol, analysis_type, base_urls):
    try:
        analysis = TA_Handler(
            symbol=symbol, screener="PAKISTAN", exchange="PSX", interval=analysis_type
        )

        if 'analysis' in locals() and analysis is not None and analysis.get_analysis() is not None:
            summary = analysis.get_analysis().summary
            indicators = analysis.get_analysis().indicators
            oscillator = analysis.get_analysis().oscillators
            moving_averages = analysis.get_analysis().moving_averages

            if summary is not None:
                buy_signal = summary['BUY']
                sell_signal = summary['SELL']
                neutral_signal = summary['NEUTRAL']
                rsi = indicators['RSI']
                rsi_last = indicators['RSI[1]']
                close = indicators['close']
                volume = indicators['volume']
                ao = indicators['AO']
                change = indicators['change']
                adx = indicators['ADX']

                return (
                    symbol, summary, close, sell_signal, neutral_signal, buy_signal,
                    volume, adx, rsi, rsi_last, ao, change, base_urls
                )

    except Exception as e:
        error_message = f"Exception occurred for symbol: {symbol}. Error Message: {e}"
        logging.error(f"{datetime.datetime.now()} - {error_message}")
        print(error_message)
    return None

def send_email(subject, body, attachment_path=None):
    # ... (Email sending logic remains unchanged)

def main():
    volume_threshold = 1000000
    ao_threshold = 0
    base_urls = [
        "https://www.tradingview.com/chart/ZMYE714n/?symbol=PSX%3A",  # Charts
        "https://www.tradingview.com/symbols/PSX-",  # Finance
        "https://www.tradingview.com/symbols/PSX-"  # Tech
    ]

    symbol_lists = {
        "KMIALL": KMIALL,
        "KMI100": KMI100,
        "KMI30": KMI30,
        "MYLIST": MYLIST,
        "QSE": QSE
    }

    time_frames = ["1M", "1W", "1D", "4H"]
    recommendation_options = ["STRONG_BUY", "BUY", "NEUTRAL", "SELL", "STRONG_SELL"]

    while True:
        current_datetime = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        print(f"Technical Analysis Date and Time: {current_datetime}")

        for analysis_type in time_frames:
            for recommendation_filter in recommendation_options:
                analyzed_data = []

                with ThreadPoolExecutor(max_workers=500) as executor:
                    for symbol_selection, psx_symbols in symbol_lists.items():
                        futures = [
                            executor.submit(analyze_symbol, symbol, analysis_type, base_urls)
                            for symbol in psx_symbols
                        ]

                        for future in futures:
                            result = future.result()
                            if result:
                                analyzed_data.append(result)

                # ... (Data export and email sending logic remains unchanged)

        print("Sleeping for 24 hours...")
        time.sleep(86400)  # Sleep for 24 hours

if __name__ == "__main__":
        main()
