import time
import pandas as pd
from tradingview_ta import TA_Handler, Interval
from email_functions import send_email   # Import the send_email function from the send_email.py file

symbol_selection = [
    "ABOT","AGP","AGSML","APL","ARPL","ASL","ATRL","AVN","BIFO","BIPL","BNWM","BWCL","CEPB","CHCC","COLG","DAWH","DCR","DGKC","DOL","DYNO","EFERT","ENGRO","ENGRO",
    "EPCL","FABL","FATIMA","FCCL","FCEPL","FFBL","FHAM","GHGL","GLAXO","HINOON","HUBC","ICL","ILP","IMAGE","INIL","ISL","JVDC","KEL","KOHC","KTML",
    "LCI","LOTCHEM","LUCK","MARI","MEBL","MLCF","MTL","MUGHAL","MZNPETF","NESTLE","NETSOL","NML","NRL","OGDC","PABC","PAEL","PIBTL","PIOC","PKGP","PKGS","POML","PPL",
    "PSEL","PSO","PTCA","QUICE","RMPL","SAZEW","SEARL","SHEL","SHFA","SNGP","SPL","STCL","SYS","TGL","THALL","UNITY","WAVES","WHALE","WTL","KSE100","KSE30","KSEALL","KSEALLSHR"
]

all_time_frames = [
    Interval.INTERVAL_4_HOURS,
    Interval.INTERVAL_1_DAY,
    Interval.INTERVAL_1_WEEK,
    Interval.INTERVAL_1_MONTH,
]

# Initialize an empty DataFrame to store the data
data = pd.DataFrame(columns=['Symbol', 'Timestamp', 'Recommendation', 'Close', 'RSI', 'AO', 'Volume'])

while True:
    try:
        for symbol in symbol_selection:
            strong_buy_count = 0
            strong_sell_count = 0
            all_time_frames_recommendations = []
            all_time_frames_rsi = []
            all_time_frames_ao = []
            all_time_frames_volume = []
            all_time_frames_close = []

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
                    close = indicators['close']()
                    all_time_frames_close.append(close)
                    ao = indicators['AO']
                    all_time_frames_ao.append(ao)
                    volume = indicators['volume']()
                    all_time_frames_volume.append(volume)
                    if summary == 'STRONG_BUY':
                        strong_buy_count += 1
                    elif summary == 'STRONG_SELL':
                        strong_sell_count += 1

                    time.sleep(5)  # Wait for 5 seconds
                except Exception as e:
                    print(f"Error for {symbol} - {time_frame}:", e)

            if strong_buy_count >= 3 or strong_sell_count >= 2:
                recommendation = "Strong Buy" if strong_buy_count >= 3 else "Strong Sell"
                timestamp = pd.Timestamp.now()
                row_data = [symbol, timestamp, recommendation, close, all_time_frames_rsi, all_time_frames_ao, all_time_frames_volume]
                data = data.append(pd.Series(row_data, index=data.columns), ignore_index=True)

                body = f"At least 3 time frames {recommendation} for {symbol} @ {close}. Recommendations (4H-1D-1W-1M): {all_time_frames_recommendations} RSI: {all_time_frames_rsi} AO: {all_time_frames_ao} Volume: {all_time_frames_volume}"
                print(body)
                subject = f"{symbol}-PSX-Technical_Analysis"
                try:
                    # Send email
                    send_email(subject, body)
                except Exception as e:
                    print(f"Error sending email: {str(e)}")

        # Save data to Excel file
        data.to_excel("crypto_analysis_data.xlsx", index=False)

        print("Waiting for 30 minutes before starting the next analysis...")
        countdown = 1800  # Set the countdown time in seconds
        while countdown > 0:
            print(f"Countdown: {countdown} seconds")
            time.sleep(1)  # Wait for 1 second
            countdown -= 1

        print("Countdown finished. Starting the next analysis...")

    except Exception as e:
        print("Error:", e)
