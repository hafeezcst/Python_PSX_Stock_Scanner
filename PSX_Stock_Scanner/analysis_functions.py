import datetime
from tradingview_ta import TA_Handler, Interval
import logging

def analyze_symbol(symbol, analysis_type, base_url_charts, base_url_finance, base_url_tech) :
    
    try :
        if analysis_type == "M" :
            analysis = TA_Handler ( symbol=symbol, screener="PAKISTAN", exchange="PSX",
                                    interval=Interval.INTERVAL_1_MONTH )
        elif analysis_type == "W" :
            analysis = TA_Handler ( symbol=symbol, screener="PAKISTAN", exchange="PSX",
                                    interval=Interval.INTERVAL_1_WEEK )
        elif analysis_type == "D" :
            analysis = TA_Handler ( symbol=symbol, screener="PAKISTAN", exchange="PSX",
                                    interval=Interval.INTERVAL_1_DAY )
        elif analysis_type == "H" :
            analysis = TA_Handler ( symbol=symbol, screener="PAKISTAN", exchange="PSX",
                                    interval=Interval.INTERVAL_1_HOUR )
        
        if 'analysis' in locals ( ) and analysis is not None and analysis.get_analysis ( ) is not None :
            summary = analysis.get_analysis ( ).summary
            indicators = analysis.get_analysis ( ).indicators
            oscillator = analysis.get_analysis ( ).oscillators
            moving_averages = analysis.get_analysis ( ).moving_averages
            
            if summary is not None :
                buy_signal = summary [ 'BUY' ]
                sell_signal = summary [ 'SELL' ]
                neutral_signal = summary [ 'NEUTRAL' ]
                rsi = indicators [ 'RSI' ]
                rsi_last = indicators [ 'RSI[1]' ]
                close = indicators [ 'close' ]
                volume = indicators [ 'volume' ]
                ao = indicators [ 'AO' ]
                change = indicators [ 'change' ]
                adx = indicators [ 'ADX' ]
                # Calculate average support and resistance
                
                fabonacciS1 = indicators['Pivot.M.Fibonacci.S1']
                fabonacciS2 = indicators['Pivot.M.Fibonacci.S2']
                fabonacciS3 = indicators['Pivot.M.Fibonacci.S3']
                fabonacciR1 = indicators['Pivot.M.Fibonacci.R1']
                fabonacciR2 = indicators['Pivot.M.Fibonacci.R2']
                fabonacciR3 = indicators['Pivot.M.Fibonacci.R3']
                classicS1 = indicators['Pivot.M.Classic.S1']
                classicS2 = indicators['Pivot.M.Classic.S2']
                classicS3 = indicators['Pivot.M.Classic.S3']
                classicR1 = indicators['Pivot.M.Classic.R1']
                classicR2 = indicators['Pivot.M.Classic.R2']
                classicR3 = indicators['Pivot.M.Classic.R3']               
                # Calculate average support and resistance
                support_values      = [fabonacciS1, fabonacciS2, fabonacciS3]
                resistance_value    = [fabonacciR1, fabonacciR2, fabonacciR3]
                Svalues = [value for value in support_values if value is not None]  # Exclude None values
                Rvalues = [value for value in resistance_value if value is not None]  # Exclude None values
                # Calculate average support and resistance
                average_support = sum(Svalues) / len(Svalues) if Svalues else None
                average_resistance = sum(Rvalues) / len(Rvalues) if Rvalues else None
                
                # Export average support and resistance to Excel
                # Add your code here to export the values to Excel
                #print ( f"Average Support: {average_support}" ) 
                #print ( f"Average Resistance: {average_resistance}" )              
                # Construct the website link
                charts = f"{base_url_charts}{symbol}"
                financials = f"{base_url_finance}{symbol}/financials-overview/"
                technicals = f"{base_url_tech}{symbol}/technicals/"
                
                #return symbol, summary, close, sell_signal, neutral_signal, buy_signal, volume, adx, rsi, rsi_last, ao, change, charts, financials, technicals
                return symbol, summary, close, sell_signal, neutral_signal, buy_signal, volume, adx, rsi, rsi_last, ao, change,average_support, average_resistance, charts, financials, technicals
    except Exception as e:
        error_message = f"Exception occurred for symbol: {symbol}. Error Message: {e}"
        logging.error ( f"{datetime.datetime.now ( )} - {error_message}" )
        print ( error_message )
    return None
