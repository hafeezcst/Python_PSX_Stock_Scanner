import time
def get_recommendation_filter():
    recommendation_options = ["STRONG_BUY", "BUY", "NEUTRAL", "SELL", "STRONG_SELL"]
    
    recommendation_filter = input(f"Select recommendation filter ({', '.join(recommendation_options)}): ").upper()
    
    if not recommendation_filter:
        time.sleep(5)
        recommendation_filter = "STRONG_BUY"
        print(f"Selected recommendation filter: {recommendation_filter}")

    while recommendation_filter not in recommendation_options:
        print("Invalid recommendation filter. Please try again.")
        recommendation_filter = input(f"Select recommendation filter ({', '.join(recommendation_options)}): ").upper()

    return recommendation_filter