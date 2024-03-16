import time
import csv
from datetime import datetime
from tradingview_ta import TA_Handler, Interval
from email_functions import send_email
from Create_crypto_list import create_crypto_list
symbol_selection = create_crypto_list()

all_time_frames = [

    Interval.INTERVAL_1_HOUR,
    Interval.INTERVAL_4_HOURS,
    Interval.INTERVAL_1_DAY,
    Interval.INTERVAL_1_WEEK,
    Interval.INTERVAL_1_MONTH,
]

while True:
    try:
        for symbol in symbol_selection:
            strong_buy_count = 0
            strong_sell_count = 0
            all_time_frames_recommendations = []
            all_time_frames_rsi = []
            all_time_frames_ao = []
            all_time_frames_volume = []
            all_time_frames_change = []

            print(f"Analyzing {symbol}...")

            for time_frame in all_time_frames:
                try:
                    analysis = TA_Handler(
                        symbol=symbol,
                        screener="CRYPTO",
                        exchange="BINANCE",
                        interval=time_frame,
                    )
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    summary = analysis.get_analysis().summary['RECOMMENDATION']
                    all_time_frames_recommendations.append(summary)
                    indicators = analysis.get_analysis().indicators
                    rsi = indicators['RSI']
                    all_time_frames_rsi.append(rsi)
                    high = indicators['high']
                    close = indicators['close']
                    low = indicators['low']
                    change = indicators['change']
                    all_time_frames_change.append(change)
                    volume = indicators['volume']
                    all_time_frames_volume.append(volume)
                    ao = indicators['AO']
                    all_time_frames_ao.append(ao)
                    if summary == 'STRONG_BUY':
                        strong_buy_count += 1
                    elif summary == 'STRONG_SELL':
                        strong_sell_count += 1
                    time.sleep(1)  # Wait for 1 second
                except Exception as e:
                    print(f"Error for {symbol} - {time_frame}:", e)

            if strong_buy_count >= 4 or strong_sell_count >= 2:
                recommendation = "Strong Buy" if strong_buy_count >= 4 else "Strong Sell"
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                row_data = [timestamp, symbol, close, all_time_frames_recommendations, all_time_frames_change, all_time_frames_rsi, all_time_frames_ao, all_time_frames_volume]
                with open('Crypto Analysis_Data.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(row_data)
                
                body = f"At least 4 time frames {recommendation} for {symbol} @ {close}. Recommendations (15M-1H-4H-1D-1W-1M): {all_time_frames_recommendations} Change: {all_time_frames_change} RSI: {all_time_frames_rsi} AO: {all_time_frames_ao} Volume: {all_time_frames_volume}"
                print(body)
                subject = f"{symbol}-{recommendation} CRYOTO-Technical_Analysis"
                try:
                    # Send email
                    send_email(subject, body)
                except Exception as e:
                    print(f"Error sending email: {str(e)}")
                    
        print("Waiting for 15 minutes before starting the next analysis...")
        countdown = 900  # Set the countdown time in seconds
        while countdown > 0:
            print(f"Countdown: {countdown} seconds")
            time.sleep(1)  # Wait for 1 second
            countdown -= 1

        print("Countdown finished. Starting the next analysis...")


    except Exception as e:
        print("Error:", e)
