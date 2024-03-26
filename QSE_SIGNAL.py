import time
from tradingview_ta import TA_Handler, Interval
from email_functions import send_email
import pandas as pd
   
   # Import the send_email function from the email_functions.py file
def get_symbol_selection():
    df = pd.read_excel('psxsymbols.xlsx', sheet_name='QSE')
    symbol_selection = df.iloc[:, 0].tolist()
    return symbol_selection

symbol_selection = get_symbol_selection()

all_time_frames = [
    #Interval.INTERVAL_5_MINUTES,
    #Interval.INTERVAL_15_MINUTES,
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
            all_time_frames_volumne = []

            print(f"Analyzing {symbol}...")

            for time_frame in all_time_frames:
                try:
                    analysis = TA_Handler(
                        symbol=symbol,
                        screener="QATAR",
                        exchange="QSE",
                        interval=time_frame,
                    )
                    summary = analysis.get_analysis().summary['RECOMMENDATION']
                    all_time_frames_recommendations.append(summary)
                    indicators = analysis.get_analysis ( ).indicators
                    rsi = indicators [ 'RSI' ]
                    all_time_frames_rsi.append(rsi)
                    high = indicators [ 'high' ]
                    close = indicators [ 'close' ]
                    low = indicators [ 'low' ]
                    volume = indicators [ 'volume' ]
                    all_time_frames_volumne.append(volume)
                    ao = indicators [ 'AO' ]
                    ao_last = indicators [ 'AO[1]' ]
                    ao_diff = ao - ao_last
                    all_time_frames_ao.append(ao)
                    if summary == 'STRONG_BUY':
                        strong_buy_count += 1
                    elif summary == 'STRONG_SELL':
                        strong_sell_count += 1
                except Exception as e:
                    print(f"Error for {symbol} - {time_frame}:", e)

            if strong_buy_count >= 4 or strong_sell_count >= 2:
                recommendation = "Strong Buy" if strong_buy_count >= 4 else "Strong Sell"
                body = f"At least 3 time frames {recommendation} for {symbol} @ {close}. Recommendations (1H-4H-1D-1W-1M): {all_time_frames_recommendations} RSI: {all_time_frames_rsi} AO: {all_time_frames_ao} Volumne: {all_time_frames_volumne}"
                print(body)
                subject = f"{symbol}-{recommendation} QSE-Technical_Analysis"
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
