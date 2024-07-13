import datetime
from tradingview_ta import TA_Handler, Interval
import logging

def analyze_symbol(symbol, analysis_type,screener_selection,exchange_selection,base_url_charts, base_url_finance, base_url_tech) :
    """
    Analyzes a stock symbol using technical analysis indicators and returns the analysis results.

    Args:
        symbol (str): The stock symbol to analyze.
        analysis_type (str): The type of analysis to perform. Valid values are "M" (monthly), "W" (weekly), "D" (daily), "H" (hourly).
        base_url_charts (str): The base URL for the charts of the stock symbol.
        base_url_finance (str): The base URL for the financials of the stock symbol.
        base_url_tech (str): The base URL for the technicals of the stock symbol.

    Returns:
        tuple: A tuple containing the following analysis results:
            - symbol (str): The stock symbol.
            - summary (dict): A dictionary containing the summary of the analysis.
            - close (float): The closing price of the stock.
            - sell_signal (int): The sell signal.
            - neutral_signal (int): The neutral signal.
            - buy_signal (int): The buy signal.
            - volume (float): The volume of the stock.
            - adx (float): The ADX (Average Directional Index) value.
            - rsi (float): The RSI (Relative Strength Index) value.
            - rsi_last (float): The previous RSI value.
            - ao (float): The AO (Awesome Oscillator) value.
            - change (float): The change in price.
            - average_support (float): The average support level.
            - average_resistance (float): The average resistance level.
            - charts (str): The URL for the charts of the stock symbol.
            - financials (str): The URL for the financials of the stock symbol.
            - technicals (str): The URL for the technicals of the stock symbol.
    """
    
    try :
        screener = screener_selection
        exchange = exchange_selection
        if analysis_type == "M" :
            analysis = TA_Handler(symbol=symbol, screener=screener, exchange=exchange,
                                  interval=Interval.INTERVAL_1_MONTH)
        elif analysis_type == "W" :
            analysis = TA_Handler ( symbol=symbol, screener=screener, exchange=exchange,
                                    interval=Interval.INTERVAL_1_WEEK )
        elif analysis_type == "D" :
            analysis = TA_Handler ( symbol=symbol, screener=screener, exchange=exchange,
                                    interval=Interval.INTERVAL_1_DAY )
        elif analysis_type == "4H" :
            analysis = TA_Handler ( symbol=symbol, screener=screener, exchange=exchange,
                                    interval=Interval.INTERVAL_4_HOURS )
        elif analysis_type == "H" :
            analysis = TA_Handler ( symbol=symbol, screener=screener, exchange=exchange,
                                    interval=Interval.INTERVAL_1_HOUR )
        
        if 'analysis' in locals ( ) and analysis is not None and analysis.get_analysis ( ) is not None :
            summary = analysis.get_analysis ( ).summary
            indicators = analysis.get_analysis ( ).indicators
            #oscillator = analysis.get_analysis ( ).oscillators
            #moving_averages = analysis.get_analysis ( ).moving_averages
            
            if summary is not None :
                buy_signal = summary [ 'BUY' ]
                sell_signal = summary [ 'SELL' ]
                neutral_signal = summary [ 'NEUTRAL' ]
                rsi = indicators [ 'RSI' ]
                rsi_last = indicators [ 'RSI[1]' ]
                high = indicators [ 'high' ]
                close = indicators [ 'close' ]
                low = indicators [ 'low' ]
                volume = indicators [ 'volume' ]
                ao = indicators [ 'AO' ]
                change = indicators [ 'change' ]
                adx = indicators [ 'ADX' ]
                fabonacciS1 = indicators['Pivot.M.Fibonacci.S1']

                fabonacciR1 = indicators['Pivot.M.Fibonacci.R1']

                classicS1 = indicators['Pivot.M.Classic.S1']

                classicR1 = indicators['Pivot.M.Classic.R1']
              
                
                support_values      = [fabonacciS1, classicS1]
                resistance_value    = [fabonacciR1, classicR1]
                Svalues = [value for value in support_values if value is not None]  # Exclude None values
                Rvalues = [value for value in resistance_value if value is not None]  # Exclude None values
                
                average_support = sum(Svalues) / len(Svalues) if Svalues else None
                average_resistance = sum(Rvalues) / len(Rvalues) if Rvalues else None
                
                charts = f"{base_url_charts}{symbol}"
                financials = f"{base_url_finance}{symbol}/financials-overview/"
                technicals = f"{base_url_tech}{symbol}/technicals/"
                
                return symbol, summary, close, sell_signal, neutral_signal, buy_signal,volume, adx, rsi, rsi_last, ao, change,average_support, average_resistance, charts, financials, technicals
    
    except Exception as e:
        error_message = f"Exception occurred for symbol: {symbol}. Error Message: {e}"
        logging.error ( f"{datetime.datetime.now ( )} - {error_message}" )
        print ( error_message )
    return None
