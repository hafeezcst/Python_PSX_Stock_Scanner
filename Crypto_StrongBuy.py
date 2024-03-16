import time
from tradingview_ta import TA_Handler, Interval
from email_functions import send_email

symbol_selection = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT", "DOGEUSDT", "DOTUSDT", "UNIUSDT", "BCHUSDT", "LTCUSDT",
    "LINKUSDT", "XLMUSDT", "THETAUSDT", "VETUSDT", "TRXUSDT", "EOSUSDT", "XMRUSDT", "AAVEUSDT", "XTZUSDT", "ATOMUSDT",
    "NEOUSDT", "MKRUSDT", "SOLUSDT", "COMPUSDT", "FTTUSDT", "ALGOUSDT", "CROUSDT", "KSMUSDT", "LEOUSDT", "HTUSDT",
    "EGLDUSDT", "SNXUSDT", "YFIUSDT", "RUNEUSDT", "SUSHIUSDT", "AVAXUSDT", "BATUSDT", "ZECUSDT", "GRTUSDT", "MANAUSDT",
    "ENJUSDT", "CRVUSDT", "RENUSDT", "LRCUSDT", "SANDUSDT", "OCEANUSDT", "1INCHUSDT", "KNCUSDT", "STMXUSDT", "BALUSDT"
]

all_time_frames = [
    #Interval.INTERVAL_5_MINUTES,
    Interval.INTERVAL_15_MINUTES,
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
            all_time_frames_recommendations = []

            print(f"Analyzing {symbol}...")

            for time_frame in all_time_frames:
                try:
                    analysis = TA_Handler(
                        symbol=symbol,
                        screener="CRYPTO",
                        exchange="BINANCE",
                        interval=time_frame,
                    )
                    summary = analysis.get_analysis().summary['RECOMMENDATION']
                    all_time_frames_recommendations.append(summary)

                    if summary == 'STRONG_BUY':
                        strong_buy_count += 1
                except Exception as e:
                    print(f"Error for {symbol} - {time_frame}:", e)

            if strong_buy_count >= 3:
                body = f"At least 3 time frames Strong Buy for {symbol}. Recommendations: {all_time_frames_recommendations}"
                print(body)
                subject = f"Crypto-Technical_Analysis_{symbol}"
                try:
                    # Send email
                    send_email(subject, body)
                except Exception as e:
                    print(f"Error sending email: {str(e)}")

        print("Waiting for 30 minutes before starting the next analysis...")
        time.sleep(1800)  # 1800 seconds = 30 minutes

    except Exception as e:
        print("Error:", e)
