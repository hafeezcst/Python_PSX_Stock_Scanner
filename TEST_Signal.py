import time
from datetime import datetime
from tradingview_ta import TA_Handler, Interval
from email_functions import send_email
import pandas as pd


# add golbal variable for Pakisatn exchange
exchange_PSX = 'PSX'
screener_PAK = 'PAKISTAN'
sheet_name_PAK = 'KMI100'
# add golbal variable for Qatar exchange
exchange_QSE = 'QSE'
screener_QAT = 'QATAR'
sheet_name_QAT = 'QSE'
# add global variables for forex
exchange_FOREX = 'FOREX'
screener_FOREX = 'FOREX'
sheet_name_Forex = 'FOREX'
# add global variables for crypto currency
exchange_CRYPTO = 'BINANCE'
screener_CRYPTO = 'CRYPTO'
sheet_name_Crypto = 'CRYPTO'
# add global variables for indian exchange
exchange_INDIA = 'NSE'
screener_INDIA = 'INDIA'
sheet_name_India = 'NIFTY200'


    # Your code here

def get_symbol_selection():
    df = pd.read_excel('psxsymbols.xlsx', sheet_name='KMI100')
    symbol_selection = df.iloc[:, 0].tolist()
    return symbol_selection

def is_trading_hours():
    current_time = datetime.now().time()
    current_day = datetime.now().weekday()  # Monday=0, Tuesday=1, ..., Sunday=6
    trading_start_time = datetime.strptime('07:30:00', '%H:%M:%S').time()
    trading_end_time = datetime.strptime('17:30:00', '%H:%M:%S').time()
    return (0 <= current_day <= 6) and (trading_start_time <= current_time <= trading_end_time)

# Update the save_daily_report() function to use f-strings for dynamic file names
def save_daily_report(data, exchange):
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f'{exchange}-Daily_Analysis_Report.xlsx'
    try:
        existing_data = pd.read_excel(filename)
        updated_data = pd.concat([existing_data, data], ignore_index=True)
        updated_data.to_excel(filename, index=False)
    except FileNotFoundError:
        data.to_excel(filename, index=False)

symbol_selection = get_symbol_selection()

all_time_frames = [
    Interval.INTERVAL_1_DAY,
    Interval.INTERVAL_1_WEEK,
    Interval.INTERVAL_1_MONTH,
]

while True:
    try:
        if is_trading_hours():
            analysis_data = []
            for exchange, screener, sheet_name in [
                                                (exchange_PSX, screener_PAK, sheet_name_PAK),
                                                (exchange_QSE, screener_QAT, sheet_name_QAT),
                                                #    (exchange_FOREX, screener_FOREX, sheet_name_Forex),
                                                #   (exchange_CRYPTO, screener_CRYPTO, sheet_name_Crypto),
                                                #   (exchange_INDIA, screener_INDIA, sheet_name_India),
                                                ]:
                df = pd.read_excel('psxsymbols.xlsx', sheet_name=sheet_name)
                symbol_selection = df.iloc[:, 0].tolist()

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
                                screener=screener,
                                exchange=exchange,
                                interval=time_frame,
                            )
                            summary = analysis.get_analysis().summary['RECOMMENDATION']
                            all_time_frames_recommendations.append(summary)
                            indicators = analysis.get_analysis().indicators
                            rsi = indicators['RSI']
                            all_time_frames_rsi.append(rsi)
                            rsi_last = indicators['RSI[1]']  # Added to store the last RSI value
                            all_time_frames_rsi_last.append(rsi_last)
                            high = indicators['high']
                            close = indicators['close']
                            change = indicators['change']
                            all_time_frames_change.append(change)
                            low = indicators['low']
                            volume = indicators['volume']
                            all_time_frames_volume.append(volume)
                            ao = indicators['AO']
                            all_time_frames_ao.append(ao)
                            if summary in ('STRONG_BUY', 'BUY', 'NEUTRAL') and ao > 0 and volume > 50000 and rsi > rsi_last: # Added to check if RSI is increasing
                                strong_buy_count += 1
                            elif summary in ('STRONG_SELL','SELL') and ao < 0 and rsi< rsi_last: # Added to check if RSI is decreasing
                                strong_sell_count += 1
                        except Exception as e:
                            print(f"Error for {symbol} - {time_frame}:", e)

                    if strong_buy_count >= 3 or strong_sell_count >= 1:
                        recommendation = "Strong Buy" if strong_buy_count >= 3 else "Strong Sell"
                        attachment_path = ''
                        subject = f"{symbol}-{recommendation} - {datetime.now().strftime('%Y-%m-%d')}"
                        body = f"At least 3 time frames {recommendation} for {symbol} @ {close}. Recommendations (1D-1W-1M):\n {all_time_frames_recommendations}\n Change:\n {all_time_frames_change} \n RSI: \n {all_time_frames_rsi}\n AO:\n {all_time_frames_ao} \n Volume:\n {all_time_frames_volume}"
                        print(body)
                        subject = f"{symbol}-{recommendation}-Technical_Analysis"
                        try:
                            # Send email
                            #send_email(subject, body)
                            print("Email sent stopped for testing...")
                        except Exception as e:
                            print(f"Error sending email: {str(e)}")
                        analysis_data.append({
                            'Date': datetime.now().strftime('%Y-%m-%d'),
                            'Time': datetime.now().strftime('%H:%M:%S'),
                            'Symbol': symbol,
                            'Recommendation': recommendation,
                            'Close Price': close,
                            'Recommendations': all_time_frames_recommendations,  # Fixed quotation marks and added key/value pair
                            'Change': all_time_frames_change,
                            'RSI': all_time_frames_rsi,
                            'AO': all_time_frames_ao,
                            'Volume': all_time_frames_volume
                        })

            if analysis_data:
                # Create DataFrame from analysis_data
                report_df = pd.DataFrame(analysis_data)
                # Save daily report to Excel
                save_daily_report(report_df)
                # Send email with daily report
                strong_buy_df = report_df[report_df['Recommendation'] == 'Strong Buy']
                strong_buy_df = strong_buy_df.to_string(index=True, justify='left')
                strong_sell_df = report_df[report_df['Recommendation'] == 'Strong Sell']
                strong_sell_df = strong_sell_df.to_string(index=True, justify='left')
                attachment_path = '{exchange}-Daily_Analysis_Report.xlsx'
                subject = f'{exchange}-Daily Report - {datetime.now().strftime('%Y-%m-%d')}'
                report_df = report_df.to_string(index=True, justify='left')
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
            # Sleep for 60 minute and then check again
            time.sleep(3600)  # 60 seconds = 1 minute

    except Exception as e:
        print("Error:", e)
