from tradingview_ta import TA_Handler, Interval

def get_available_indicators(symbol, exchange,screener, interval):
    try:
        # Create a TA_Handler instance
        analysis = TA_Handler(symbol=symbol,screener=screener, exchange=exchange, interval=interval)
        
        # Get the available indicators for the given symbol, exchange, and interval
        analysis_result = analysis.get_analysis().indicators
        
        if analysis_result is not None:
            return analysis_result.keys()
        else:
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
symbol = "AABS"
exchange = "PSX"
screener = "Pakistan"


interval = Interval.INTERVAL_1_DAY
indicators = get_available_indicators(symbol, exchange,screener, interval)

# Print the list of available indicators
print("Available Indicators:")
if indicators:
    for indicator in indicators:
        print(indicator)
else:
    print("No indicators available.")
