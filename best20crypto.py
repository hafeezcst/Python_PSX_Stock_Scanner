import requests
import csv

# Define the CoinGecko API endpoint for fetching cryptocurrencies
url = 'https://api.coingecko.com/api/v3/coins/markets'

# Define parameters for the API request
params = {
    'vs_currency': 'usd',  # Currency to compare against (USD in this case)
    'order': 'market_cap_desc',  # Order by market capitalization
    'per_page': 20,  # Number of results per page
    'page': 1,  # Page number
    'price_change_percentage': '24h',  # Get percentage change over the last 24 hours
}

# Send GET request to the CoinGecko API
response = requests.get(url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Create a list to store cryptocurrency pairs
    crypto_pairs = []

    # Extract cryptocurrency symbols and append them to the list with 'USDT' suffix
    for crypto in data:
        symbol = crypto['symbol'].upper()
        pair_name = f"{symbol}USDT"
        crypto_pairs.append(pair_name)

    # Write the list of cryptocurrency pairs to a CSV file
    with open('top20crypto.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Pair Name'])
        writer.writerows(map(lambda x: [x], crypto_pairs))
        
    print("CSV file 'top20crypto.csv' has been created successfully.")
else:
    print("Failed to fetch data from CoinGecko API")
