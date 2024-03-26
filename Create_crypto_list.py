import requests
import csv
import os

def create_crypto_list():
    # Define the CoinGecko API endpoint for fetching cryptocurrencies
    url = 'https://api.coingecko.com/api/v3/coins/markets'

    # Define parameters for the API request
    params = {
        'vs_currency': 'usd',  # Currency to compare against (USD in this case)
        'order': 'market_cap_desc',  # Order by market capitalization
        'per_page': 5,  # Number of results per page
        'page': 1,  # Page number
        'price_change_percentage': '24h',  # Get percentage change over the last 24 hours
    }

    try:
        # Send GET request to the CoinGecko API
        response = requests.get(url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Create a set to store cryptocurrency pairs
            crypto_pairs = set()

            # Extract cryptocurrency symbols and append them to the set with 'USDT' suffix
            for crypto in data:
                symbol = crypto['symbol'].upper()
                pair_name = f"{symbol}USDT"
                crypto_pairs.add(pair_name)

            # Check if the file already exists
            if os.path.exists('top20crypto.csv'):
                # Read existing pairs from the file
                with open('top20crypto.csv', 'r', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    existing_pairs = set(row[0] for row in reader)

                # Append the changed pairs to the existing set
                crypto_pairs.update(existing_pairs)
                crypto_pairs = list(crypto_pairs)
                crypto_pairs = [pair for pair in crypto_pairs if pair not in ["Pair Name", "USDTUSDT", "USDCUSDT"]]

                

            # Write the updated list of cryptocurrency pairs to the CSV file
            with open('top20crypto.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Pair Name'])
                writer.writerows(map(lambda x: [x], crypto_pairs))
                
            print("Crypto list file 'top20crypto.csv' has been updated successfully.")
            return list(crypto_pairs)  # Convert set back to list for consistent return type
        else:
            print("Failed to fetch data from CoinGecko API")
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

# Example usage:
# crypto_list = create_crypto_list()
