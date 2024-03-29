import time
import csv
from datetime import datetime
from tradingview_ta import TA_Handler, Interval
from email_functions import send_email
from Create_crypto_list import create_crypto_list
from telegram_message import send_telegram_message
symbol_selection = create_crypto_list()
symbol_selection = ['PAXGUSDT']
# variales for buy and sell count
min_strong_buy_count=3
min_strong_sell_count=2
# Time frames for analysis
all_time_frames = [
    Interval.INTERVAL_5_MINUTES,
    Interval.INTERVAL_15_MINUTES,
    Interval.INTERVAL_30_MINUTES,
    Interval.INTERVAL_1_HOUR,
    Interval.INTERVAL_2_HOURS,
    Interval.INTERVAL_4_HOURS,
]
last_recommendation = None # Initialize last_recommendation as None at the start of your program
# Create a CSV file and write the header
while True:# Infinite loop to keep the script running
    try:# Try block to catch any errors
        for symbol in symbol_selection:# Loop through all the symbols
            strong_buy_count = 0
            strong_sell_count = 0
            all_time_frames_recommendations = []
            all_time_frames_rsi = []
            all_time_frames_ao = []
            all_time_frames_volume = []
            all_time_frames_change = []
            all_time_frames_high = []
            all_time_frames_close = []
            all_time_frames_low = []
            all_time_frames_rsi_last = []  # Added to store the last RSI value 
            all_time_frames_ao_last = []  # Added to store the last AO value
            all_time_frames_ao_diff_5 = []  # Added to store the AO difference for 5 minutes time frame
            all_time_frames_ao_diff_15 = []  # Added to store the AO difference for 15 minutes time frame
            all_time_frames_ao_diff_1_hour = []  # Added to store the AO difference for 1 hour time frame
            all_time_frames_ao_diff_4_hours = []  # Added to store the AO difference for 4 hours time frame    
            
            # Print the symbol being analyzed
            print(f"Analyzing {symbol}...")
            # Loop through all the time frames
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
                    # Get the analysis summary and store it in the all_time_frames_recommendations list
                    all_time_frames_recommendations.append(summary)
                    indicators = analysis.get_analysis().indicators #indator List avaialble https://pastebin.com/1DjWv2Hd
                    rsi = round(indicators['RSI'],2)
                    all_time_frames_rsi.append(rsi)
                    rsi_last = round(indicators['RSI[1]'],2)  # Added to store the last RSI value    
                    all_time_frames_rsi_last.append(rsi_last)
                    high = indicators['high']
                    all_time_frames_high.append(high)
                    close = round(indicators['close'],3)
                    all_time_frames_close.append(close)
                    low = indicators['low']
                    all_time_frames_low.append(low)
                    change = indicators['change']
                    all_time_frames_change.append(change)
                    volume = indicators['volume']
                    all_time_frames_volume.append(volume)
                    ao = round(indicators['AO'],3)
                    all_time_frames_ao.append(ao)
                    ao_last = indicators['AO[1]']  # Added to store the last AO val
                    all_time_frames_ao_last.append(ao_last)
                    # Get the support and resistance values
                    fabonacciS1 = indicators['Pivot.M.Fibonacci.S1']
                    fabonacciS2 = indicators['Pivot.M.Fibonacci.S2']
                    fabonacciR1 = indicators['Pivot.M.Fibonacci.R1']
                    fabonacciR2 = indicators['Pivot.M.Fibonacci.R2']                      
                    print(f"Time Frame: {time_frame} - Summary: {summary} - RSI: {rsi} - AO: {ao} -AO_LAST: {ao_last} - Volume: {volume} - Change: {change}")
                    # check if the AO is increasing or decreasing for 5 and 15 minutes time frame
                    ao_diff = {}
                    if time_frame == Interval.INTERVAL_5_MINUTES:
                        ao_diff['5_minutes'] = ao - ao_last
                        ao_diff_5 = round(ao_diff['5_minutes'],4)

                    if time_frame == Interval.INTERVAL_15_MINUTES:
                        ao_diff['15_minutes'] = ao - ao_last
                        ao_diff_15 = round(ao_diff['15_minutes'],4)
                        print(f"AO_DIFF_15: {ao_diff_15}")
                        fabonacciS1_SL1 = indicators['Pivot.M.Fibonacci.S1']
                        fabonacciS2_SL2 = indicators['Pivot.M.Fibonacci.S2']
                        fabonacciR1_TP1 = indicators['Pivot.M.Fibonacci.R1']
                        fabonacciR2_TP2 = indicators['Pivot.M.Fibonacci.R2']
                    if time_frame == Interval.INTERVAL_30_MINUTES:
                        ao_diff['30_minutes'] = ao - ao_last
                        ao_diff_30 = round(ao_diff['30_minutes'],4)
                        
                    if time_frame == Interval.INTERVAL_1_HOUR:
                        ao_diff['1_hour'] = ao - ao_last
                        ao_diff_1_hour = round(ao_diff['1_hour'],4)

                    if time_frame == Interval.INTERVAL_2_HOURS:
                        ao_diff['2_hours'] = ao - ao_last
                        ao_diff_2_hour = round(ao_diff['2_hours'],4)

                    if time_frame == Interval.INTERVAL_4_HOURS:
                        ao_diff['4_hours'] = ao - ao_last
                        ao_diff_4_hours = round(ao_diff['4_hours'],4) 

                    # Check the conditions for strong buy or strong sell
                    if summary in ('STRONG_BUY','BUY','NEUTRAL') and ao_diff_15 > 0 and  rsi >= 30:
                            strong_buy_count += 1
                    elif summary in ('STRONG_SELL','SELL','NEUTRAL') and ao_diff_5 < 0 and  rsi <= 70:
                            strong_sell_count += 1
                    time.sleep(2)  # Wait for 2 second
                except Exception as e:
                    print(f"Error for {symbol} - {time_frame}:", e)
            # Check if the strong buy or strong sell count is greater than or equal to 2
                    # At the beginning of your script, initialize an empty list to track open trades
                open_trades = []  # Existing open trades
                closed_trades_pnl = []  # Store P&L for closed trades
            # Initialize last_recommendation as None at the start of your program


            if strong_buy_count >= min_strong_buy_count or strong_sell_count >= min_strong_sell_count:
                recommendation = "Strong Buy" if strong_buy_count >= min_strong_buy_count else "Strong Sell" #recommendation_options = ["STRONG_BUY", "BUY", "NEUTRAL", "SELL", "STRONG_SELL"]
                print(f"Recommendation for {symbol}: {recommendation}")
                # Only send a message if the recommendation has changed
                if recommendation != last_recommendation:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
                    average_ao_diff = round(((ao_diff_5 + ao_diff_15 + ao_diff_1_hour + ao_diff_4_hours) / 4),3) 
                    message =f"Starting Trading Analysis (from updated logic) at -: {timestamp}\n"
                    message += f"{symbol}: {recommendation} @ Close: {close}\n"
                    message += f"Recommendations:{all_time_frames} - {all_time_frames_recommendations}\n"
                    message += f"RSI: {all_time_frames_rsi}\n"
                    message += f"AO_Diff_5: {ao_diff_5}\n"
                    message += f"AO_Diff_15: {ao_diff_15}\n"
                    message += f"Average_AO_Diff: {average_ao_diff}\n"
                    if recommendation == "Strong Buy":
                        message += f"TP1: {fabonacciR1_TP1} and TP2: {fabonacciR2_TP2}\n"
                        message += f"SL1: {fabonacciS1_SL1} and SL2: {fabonacciS2_SL2}\n"
                    elif recommendation == "Strong Sell":
                        message += f"SL1: {fabonacciR1_TP1} and SL2: {fabonacciR2_TP2}\n"
                        message += f"TP1: {fabonacciS1_SL1} and TP2: {fabonacciS2_SL2}\n"
                    try:
                        send_telegram_message(message)
                        print("Telegram message sent successfully")
                    except Exception as e:
                        print("Error sending Telegram message:", e)  
                
                # Update last_recommendation
                last_recommendation = recommendation                            
                # Define a function to calculate the P&L for a trade
                def calculate_pnl(entry_price, exit_price, direction, lot_size):
                    if direction == "BUY":
                        return (exit_price - entry_price) * lot_size
                    else:  # direction == "SELL"
                        return (entry_price - exit_price) * lot_size
               
               # Inside your main analysis loop, after determining the signal (strong buy or strong sell)
                if recommendation == "Strong Buy":
                    # Check if there is already an open buy trade for this symbol
                    open_trade = next((trade for trade in open_trades if trade['symbol'] == symbol and trade['direction'] == 'BUY'), None)
                    if not open_trade:
                        # No open buy trade, simulate opening a new trade
                        open_trades.append({
                            'symbol': symbol,
                            'entry_price': close,
                            'lot_size': 3,  # Fixed lot size for gold
                            'direction': 'BUY'
                        })
                        print(f"Simulated opening BUY trade for {symbol} at {close}")

                elif recommendation == "Strong Sell":
                    # Check if there is an open buy trade for this symbol
                    open_trade = next((trade for trade in open_trades if trade['symbol'] == symbol and trade['direction'] == 'BUY'), None)
                    if open_trade:
                        # Calculate P&L for the closed buy trade
                        pnl = calculate_pnl(open_trade['entry_price'], close, 'BUY', open_trade['lot_size'])
                        closed_trades_pnl.append(pnl)
                        # Simulate closing the buy trade
                        print(f"Simulated closing BUY trade for {symbol} at {close} with P&L: {pnl}")
                        open_trades.remove(open_trade)
                        # Simulate opening a new sell trade
                        open_trades.append({
                            'symbol': symbol,
                            'entry_price': close,
                            'lot_size': 3,
                            'direction': 'SELL'
                        })
                        print(f"Simulated opening SELL trade for {symbol} at {close}")
                # Update to show current and booked P&L
                booked_pnl = sum(closed_trades_pnl)
                print(f"Total booked P&L: {booked_pnl}")
                for trade in open_trades:
                    current_pnl = calculate_pnl(trade['entry_price'], close, trade['direction'], trade['lot_size'])
                    print(f"Current P&L for open {trade['direction']} trade for {trade['symbol']} is {current_pnl}")               
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                row_data = [timestamp, symbol, close, all_time_frames_recommendations, all_time_frames_change, all_time_frames_rsi, all_time_frames_ao,all_time_frames_ao_last,all_time_frames_ao_diff_15, all_time_frames_volume]
                row_data +=[average_ao_diff,open_trades,closed_trades_pnl,booked_pnl]
                with open('Crypto Analysis_Data.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(row_data)
                body = f"Target-75 PIPs (3-lot Gold) to be achieved in 24 hours\n"
                body += f"At least {min_strong_buy_count} time frames: AO_DIFF_15M: {ao_diff_15}\n {recommendation} for {symbol} @ {close}. Recommendations: {all_time_frames}: \n {all_time_frames_recommendations} \n Change:{all_time_frames_change}\n RSI: {all_time_frames_rsi} \n AO: {all_time_frames_ao} \n Volume: {all_time_frames_volume}\n"
                body += f"average_ao_diff: {average_ao_diff}\n"
                body += f"\n Open Trades: {open_trades}\n Closed Trades P&L: {closed_trades_pnl}\n"
                body += f"\n Total booked P&L: {booked_pnl}"
                subject = f"{symbol} - CRYOTO-Technical_Analysis"
                try:
                    # Send email
                    #send_email(subject, body)
                    print("Email sent successfully!")
                except Exception as e:
                    print(f"Error sending email: {str(e)}")
                    
        countdown = 30  # Set the countdown time in seconds (1 minutes)
        print(f"Waiting for {countdown} seconds before starting the next analysis...")
        while countdown > 0:
            minutes = countdown // 60
            seconds = countdown % 60
            print(f"Next Analysis: {minutes} minutes {seconds} seconds")
            time.sleep(1)  # Wait for 1 second
            countdown -= 1

        print("Countdown finished. Starting the next analysis...")

    except Exception as e:
        print("Error:", e)
