import time
from datetime import datetime
from tradingview_ta import TA_Handler, Interval
from email_functions import send_email
import pandas as pd

def get_symbol_selection():
    df = pd.read_excel('psxsymbols.xlsx', sheet_name='KMI100')
    symbol_selection = df.iloc[:, 0].tolist()
    return symbol_selection

def is_trading_hours():
    current_time = datetime.now().time()
    current_day = datetime.now().weekday()  # Monday=0, Tuesday=1, ..., Sunday=6
    trading_start_time = datetime.strptime('05:00:00', '%H:%M:%S').time()
    trading_end_time = datetime.strptime('23:30:00', '%H:%M:%S').time()
    return (current_day in [6, 0, 1, 2, 3]) and (trading_start_time <= current_time <= trading_end_time)

def save_daily_report(data):
    today = datetime.now().strftime('%Y-%m-%d')
    filename = 'PSX-Daily_Analysis_Report.xlsx'
    try:
        # Load existing data if file exists
        existing_data = pd.read_excel(filename)
        # Append new data to existing data
        updated_data = pd.concat([existing_data, data], ignore_index=True)
        # Save updated data to Excel
        updated_data.to_excel(filename, index=False)
    except FileNotFoundError:
        # If file doesn't exist, save data to a new file
        data.to_excel(filename, index=False)

symbol_selection = get_symbol_selection()

all_time_frames = [
    Interval.INTERVAL_4_HOURS,
    Interval.INTERVAL_1_DAY,
    Interval.INTERVAL_1_WEEK,
    Interval.INTERVAL_1_MONTH,
]

while True:
    try:
        if is_trading_hours():
            analysis_data = []
            for symbol in symbol_selection:
                strong_buy_count = 0
                strong_sell_count = 0
                all_time_frames_recommendations = []
                all_time_frames_rsi = []
                all_time_frames_ao = []
                all_time_frames_volume = []
                all_time_frames_change = []
                all_time_frames_rsi_last = []  # Added to store the last RSI value
                print(f"Analyzing {symbol}...")

                for time_frame in all_time_frames:
                    try:
                        analysis = TA_Handler(
                            symbol=symbol,
                            screener="PAKISTAN",
                            exchange="PSX",
                            interval=time_frame,
                        )
                        summary = analysis.get_analysis().summary['RECOMMENDATION']
                        all_time_frames_recommendations.append(summary)
                        indicators = analysis.get_analysis().indicators
                        rsi = indicators['RSI']
                        all_time_frames_rsi.append(rsi)
                        rsi_last = indicators['RSI[1]']  # Added to store the last RSI value
                        high = indicators['high']
                        close = indicators['close']
                        change = indicators['change']
                        all_time_frames_change.append(change)
                        low = indicators['low']
                        volume = indicators['volume']
                        all_time_frames_volume.append(volume)
                        ao = indicators['AO']
                        all_time_frames_ao.append(ao)
                        if summary in ('STRONG_BUY', 'BUY', 'NEUTRAL',"SELL") and ao > 0 and rsi > 50 and rsi   > rsi_last:
                            strong_buy_count += 1
                        elif summary in ('STRONG_SELL','SELL',"NEUTRAL") and ao < 0 and rsi < 50:
                            strong_sell_count += 1
                        time.sleep(10)  # Wait for 10 secon
                    except Exception as e:
                        print(f"Error for {symbol} - {time_frame}:", e)

                if strong_buy_count >= 4 or strong_sell_count >= 1:
                    recommendation = "Strong Buy" if strong_buy_count >= 3 else "Strong Sell"
                    analysis_data.append({
                        'Date': datetime.now().strftime('%Y-%m-%d'),
                        'Time': datetime.now().strftime('%H:%M:%S'),
                        'Symbol': symbol,
                        'Recommendation': recommendation,
                        'Close Price': close,
                        'Recommendations': all_time_frames_recommendations,  # Fixed quotation marks and added key/value pair
                        'Change': all_time_frames_change,
                        'RSI': all_time_frames_rsi,
                        'RSI_last': all_time_frames_rsi_last,  # Added to store the last RSI value
                        'AO': all_time_frames_ao,
                        'Volume': all_time_frames_volume
                    })

            if analysis_data:
                # Create DataFrame from analysis_data
                report_df = pd.DataFrame(analysis_data)
                # Save daily report to Excel
                save_daily_report(report_df)
                # Send email with daily report
                strong_buy_df = report_df[report_df['Recommendation'] == 'Strong Buy' ]
                strong_buy_df= strong_buy_df.to_string( index=True, justify='left')
                strong_sell_df = report_df[report_df['Recommendation'] == 'Strong Sell']
                strong_sell_df= strong_sell_df.to_string( index=True, justify='left')
                attachment_path = 'PSX-Daily_Analysis_Report.xlsx'
                subject = f"PSX-Daily Report - {datetime.now().strftime('%Y-%m-%d')}"
                report_df = report_df.to_string( index=True, justify='left')
                body = f"Please find attached the daily report for further analysis.\n\n Buy and Hold Scripts:\n {strong_buy_df} \n\n Immediate Sell Scripts: \n {strong_sell_df}"
                try:
                    send_email(subject, body, attachment_path)
                except Exception as e:
                    print(f"Error sending email: {str(e)}")
                
            print("Waiting for 240 minutes before starting the next analysis...")
            time.sleep(14400)  # 1800 seconds = 30 minutes
            print("Countdown finished. Starting the next analysis...")
        else:
            current_time = datetime.now().strftime('%H:%M:%S')
            current_day = datetime.now().strftime('%A')
            print(f"Currently not trading hours or trading day. Current time: {current_time} - {current_day} Waiting for 10 minute before checking again...")
            # Sleep for 1 minute and then check again
            time.sleep(600)  # 60 seconds = 1 minute

    except Exception as e:
        print("Error:", e)
