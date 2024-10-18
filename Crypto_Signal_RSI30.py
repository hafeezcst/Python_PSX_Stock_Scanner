import time,math
import csv
from datetime import datetime
from tradingview_ta import TA_Handler, Interval
from email_functions import send_email
from Create_crypto_list import create_crypto_list
from telegram_message import send_telegram_message
# create a list of crypto symbols to analyze
symbol_selection = create_crypto_list ( )
# symbol selection for testing
symbol_selection = ['PAXGUSDT']
# fixed price difference between the close and the binance (PAXGUSDT) and actual price (XAUUSD)
PriceDelta=0 # Price difference between the close and the binance and aacual price
#**************************************************************************************
# initialize and login to MetaTrader5

# variables for buy and sell count
min_strong_buy_count = 3
min_strong_sell_count = 3
# Time frames for analysis
all_time_frames = [
    Interval.INTERVAL_5_MINUTES,
    Interval.INTERVAL_15_MINUTES,
    Interval.INTERVAL_30_MINUTES,
    Interval.INTERVAL_1_HOUR,
    Interval.INTERVAL_2_HOURS,
    Interval.INTERVAL_4_HOURS,
]
# last recommendation for the symbol
last_recommendations = {}  # Example: {'BTCUSDT': 'Strong Buy', 'ETHUSDT': 'Strong Sell'}
# Create a CSV file and write the header
while True :  # Infinite loop to keep the script running
    try :  # Try block to catch any errors
        for symbol in symbol_selection :  # Loop through all the symbols
            strong_buy_count = 0
            strong_sell_count = 0
            all_time_frames_recommendations = [ ]
            all_time_frames_rsi = [ ]
            all_time_frames_ao = [ ]
            all_time_frames_volume = [ ]
            all_time_frames_change = [ ]
            all_time_frames_high = [ ]
            all_time_frames_close = [ ]
            all_time_frames_low = [ ]
            all_time_frames_ao_diff = [ ]  # Added to store the last ao difference
            all_time_frames_rsi_last = [ ]  # Added to store the last RSI value
            all_time_frames_ao_last = [ ]  # Added to store the last AO value
            all_time_frames_ao_diff_5 = [ ]  # Added to store the AO difference for 5 minutes time frame
            all_time_frames_ao_diff_15 = [ ]  # Added to store the AO difference for 15 minutes time frame
            all_time_frames_ao_diff_1_hour = [ ]  # Added to store the AO difference for 1 hour time frame
            all_time_frames_ao_diff_4_hours = [ ]  # Added to store the AO difference for 4 hours time frame
            all_time_frames_macd = [ ]  # Added to store the MACD value
            all_time_frames_stoch = [ ]  # Added to store the Stoch value
            all_time_frames_adx = [ ]  # Added to store the ADX value
            # Print the symbol being analyzed
            print ( f"Analyzing {symbol}..." )
            # Loop through all the time frames
            for time_frame in all_time_frames :
                try :
                    analysis = TA_Handler (
                        symbol=symbol,
                        screener="CRYPTO",
                        exchange="BINANCE",
                        interval=time_frame,
                    )
                    timestamp = datetime.now ( ).strftime ( "%Y-%m-%d %H:%M:%S" )
                    summary = analysis.get_analysis ( ).summary [ 'RECOMMENDATION' ]
                    # Get the analysis summary and store it in the all_time_frames_recommendations list
                    all_time_frames_recommendations.append ( summary )
                    indicators = analysis.get_analysis ( ).indicators  # indator List avaialble https://pastebin.com/1DjWv2Hd
                    # Fetch the RSI
                    rsi = round ( indicators [ 'RSI' ], 2 )
                    all_time_frames_rsi.append ( rsi )
                    # Fetch the RSI last value
                    rsi_last = round ( indicators [ 'RSI[1]' ], 2 )  # Added to store the last RSI value
                    all_time_frames_rsi_last.append ( rsi_last )
                    # Fetch the high
                    high = round(indicators [ 'high' ], 2)
                    all_time_frames_high.append ( high )
                    # Fetch the close
                    close = round ( indicators [ 'close' ], 2 )
                    close = close + PriceDelta
                    all_time_frames_close.append ( close )
                    # Fetch the low
                    low = round(indicators [ 'low' ], 2)
                    all_time_frames_low.append ( low )
                    # Fetch the change
                    change = round(indicators [ 'change' ], 2)
                    all_time_frames_change.append ( change )
                    # Fetch the volume
                    volume = indicators [ 'volume' ]
                    all_time_frames_volume.append ( volume )
                    # Fetch the AO
                    ao = round ( indicators [ 'AO' ], 2 )
                    all_time_frames_ao.append ( ao )
                    # Fetch the AO last value
                    ao_last = round(indicators [ 'AO[1]' ], 2)  # Added to store the last AO val
                    all_time_frames_ao_last.append ( ao_last )
                    # Fetch the MACD
                    macd = round(indicators [ 'MACD.macd' ], 2)
                    all_time_frames_macd.append ( macd )
                    
                    # Fetch the Stoch
                    stoch = round(indicators [ 'Stoch.K' ], 2)
                    all_time_frames_stoch.append ( stoch )
                    # Fecth the adx
                    adx = round(indicators [ 'ADX' ], 2)
                    all_time_frames_adx.append ( adx )
                    # Get the support and resistance values
                    fabonacciS1 = round(indicators [ 'Pivot.M.Fibonacci.S1' ]+PriceDelta, 2)
                    fabonacciS2 = round(indicators [ 'Pivot.M.Fibonacci.S2' ]+PriceDelta, 2)
                    fabonacciR1 = round(indicators [ 'Pivot.M.Fibonacci.R1' ]+PriceDelta, 2)
                    fabonacciR2 = round(indicators [ 'Pivot.M.Fibonacci.R2' ]+PriceDelta, 2)
                    print (
                        f"Time Frame: {time_frame} - Summary: {summary} - RSI: {rsi} - AO: {ao} -AO_LAST: {ao_last} - Volume: {volume} - Change: {change}" )
                    # check if the AO is increasing or decreasing for 5 and 15 minutes time frame
                    ao_diff = {}
                    if time_frame == Interval.INTERVAL_5_MINUTES :
                        ao_diff [ '5_minutes' ] = ao - ao_last
                        ao_diff_5 = round ( ao_diff [ '5_minutes' ], 3 )
                        all_time_frames_ao_diff.append(ao_diff_5)  # Added to store the last ao difference
                        adx_5 = round(adx,2)
                        print ( f"ADX_5: {adx_5}" )   
                        print ( f"AO_DIFF_5: {ao_diff_5}" )
                        fabonacciS1_TP1_Sell = fabonacciS1
                        fabonacciS2_TP2_Sell = fabonacciS2
                        fabonacciR1_SL1_Sell = fabonacciR1
                        fabonacciR2_SL2_Sell = fabonacciR2
                    if time_frame == Interval.INTERVAL_15_MINUTES :
                        ao_diff [ '15_minutes' ] = ao - ao_last
                        ao_diff_15 = round ( ao_diff [ '15_minutes' ], 3 )
                        all_time_frames_ao_diff.append(ao_diff_15)
                        adx_15 = round(adx,2)
                        print ( f"ADX_15: {adx_15}" ) 
                        print ( f"AO_DIFF_15: {ao_diff_15}" )
                        fabonacciS1_SL1_Buy = fabonacciS1
                        fabonacciS2_SL2_Buy = fabonacciS2
                        fabonacciR1_TP1_Buy = fabonacciR1
                        fabonacciR2_TP2_Buy = fabonacciR2
                    if time_frame == Interval.INTERVAL_30_MINUTES :
                         ao_diff [ '30_minutes' ] = ao - ao_last
                         ao_diff_30 = round ( ao_diff [ '30_minutes' ], 3 )
                         all_time_frames_ao_diff.append(ao_diff_30)
                    if time_frame == Interval.INTERVAL_1_HOUR :
                         ao_diff [ '1_hour' ] = ao - ao_last
                         ao_diff_1_hour = round ( ao_diff [ '1_hour' ], 3 )
                         print ( f"AO_DIFF_1H: {ao_diff_1_hour}" )
                         all_time_frames_ao_diff.append(ao_diff_1_hour)
                    if time_frame == Interval.INTERVAL_2_HOURS :
                         ao_diff [ '2_hours' ] = ao - ao_last
                         ao_diff_2_hour = round ( ao_diff [ '2_hours' ], 3 )
                         print ( f"AO_DIFF_2H: {ao_diff_2_hour}" )
                         all_time_frames_ao_diff.append(ao_diff_2_hour)
                    if time_frame == Interval.INTERVAL_4_HOURS :
                         ao_diff [ '4_hours' ] = ao - ao_last
                         ao_diff_4_hours = round ( ao_diff [ '4_hours' ], 3 )
                         print ( f"AO_DIFF_4H: {ao_diff_4_hours}" )
                         all_time_frames_ao_diff.append(ao_diff_4_hours)
                    # Define the time periods in minutes
                    time_periods = [5, 15, 30, 60, 120, 240]

                    # Calculate weights using the Wiight formula
                    weights = []
                    for t in time_periods:
                        weight = (1 / math.log(t)) ** 2
                        weights.append(weight)

                    # Normalize weights so they sum to 1
                    total_weight = sum(weights)
                    normalized_weights = [w / total_weight for w in weights]

                    # Apply weights to the differences
                    weighted_ao_diff_5 = ao_diff_5 * normalized_weights[0]
                    weighted_ao_diff_15 = ao_diff_15 * normalized_weights[1]
                    weighted_ao_diff_30 = ao_diff_30 * normalized_weights[2]
                    weighted_ao_diff_1_hour = ao_diff_1_hour * normalized_weights[3]
                    weighted_ao_diff_2_hour = ao_diff_2_hour * normalized_weights[4]
                    weighted_ao_diff_4_hours = ao_diff_4_hours * normalized_weights[5]

                    # Calculate the average of the normalized differences
                    average_ao_diff = round((weighted_ao_diff_5 + weighted_ao_diff_15 + weighted_ao_diff_30+weighted_ao_diff_1_hour+weighted_ao_diff_2_hour+weighted_ao_diff_4_hours), 3)

                    #average_ao_diff = round ( ((ao_diff_5 + ao_diff_15 + ao_diff_1_hour + ao_diff_4_hours) / 4), 3 )
                    print ( f"Average_AO_Diff (5,15,30,1H,2H,4H): {average_ao_diff}" )  
                        # Check the conditions for strong buy or strong sell
                    if summary in ('STRONG_BUY','BUY') and average_ao_diff >= 0 and rsi_last > 55:
                            strong_buy_count += 1
                    elif summary in ('SELL','STRONG_SELL') and average_ao_diff <= 0 and rsi_last < 50:
                            strong_sell_count += 1
                    time.sleep(2)  # Wait for 2 second
                except Exception as e :
                    print ( f"Error for {symbol} - {time_frame}:", e )
                
            if strong_buy_count >= min_strong_buy_count or strong_sell_count >= min_strong_sell_count :
                recommendation = "Strong Buy" if strong_buy_count >= min_strong_buy_count else "Strong Sell"  # recommendation_options = ["STRONG_BUY", "BUY", "NEUTRAL", "SELL", "STRONG_SELL"]
                print ( f"Recommendation for {symbol}: {recommendation}" )
                # Only send a message if the recommendation has changed
                if symbol not in last_recommendations or recommendation != last_recommendations [ symbol ] :
                    timestamp = datetime.now ( ).strftime ( "%Y-%m-%d %H:%M:%S" )
                    message = f"IMAC-27, Starting Trading Analysis at -: {timestamp} with Target-75 PIPs (3-lot Gold) to be achieved in 24 hours\n"
                    message += f"{symbol}: {recommendation} @ Close: {close}\n"
                    message += f"Recommendations:{all_time_frames} - {all_time_frames_recommendations}\n"
                    message += f"RSI: {all_time_frames_rsi}\n"
                    message += f"AO_Diff_5(buy): {ao_diff_5}\n"
                    message += f"AO_Diff_5 (sell) {ao_diff_5}\n"
                    message += f"AO: {all_time_frames_ao}\n"
                    message += f"AO_Difference: {all_time_frames_ao_diff}\n"                 
                    message += f"Average_AO_Diff: {average_ao_diff}\n"
                    if recommendation == "Strong Buy" :
                        message += f"TP1: {fabonacciR1_TP1_Buy} and TP2: {fabonacciR2_TP2_Buy}\n"
                        message += f"SL1: {fabonacciS1_SL1_Buy} and SL2: {fabonacciS2_SL2_Buy}\n"
                    elif recommendation == "Strong Sell" :
                        message += f"TP1: {fabonacciS1_TP1_Sell} and TP2: {fabonacciS2_TP2_Sell}\n"
                        message += f"SL1: {fabonacciR1_SL1_Sell} and SL2: {fabonacciR2_SL2_Sell}\n"
                    try :
                        send_telegram_message ( message )
                        print ( "Telegram message sent successfully" )
                    except Exception as e :
                        print ( "Error sending Telegram message:", e )
                    # Send an email with the analysis details
                    body =  f" Target-75 PIPs (3-lot Gold) to be achieved in 24 hours\n"
                    body += f" At least {min_strong_buy_count} time frames: AO_DIFF_15M: {ao_diff_15}\n" 
                    body += f" {recommendation} for {symbol} @ {close}. Recommendations: {all_time_frames}: \n{all_time_frames_recommendations} \n"
                    body += f" Change:{all_time_frames_change}\n" 
                    body += f" RSI: {all_time_frames_rsi} \n AO: {all_time_frames_ao} \n Volume: {all_time_frames_volume}\n"
                    body += f" Average_ao_diff: {average_ao_diff}\n"
                    subject = f" {symbol} - Gold-Technical_Analysis"
                    try :
                    #  Send email
                        # send_email(subject, body)
                        print ( "Email processed successfully!" )
                    except Exception as e :
                        print ( f"Error sending email: {str ( e )}" )
                        
                        # Update the last recommendation for the symbol
                    last_recommendations [ symbol ] = recommendation
                    print ( f"Last Recommendation: {last_recommendations}" )
                    # Define a function to calculate the P&L for a trade
                
        def countdown_timer(seconds):
            print(f"Waiting for {seconds}            before starting the next analysis...", end="")
            while seconds > 0:
                print(f"\rNext Analysis: {seconds} seconds ", end="", flush=True)
                time.sleep(1)
                seconds -= 1
            print("\nCountdown finished. Starting the next analysis...")

        # Call the function with the desired countdown time
        countdown_timer(60)
    
    except Exception as e :
        print ( "Error:", e )
