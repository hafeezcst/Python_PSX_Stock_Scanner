import requests
from bs4 import BeautifulSoup

# Define the base URL
base_url = "https://www.investing.com"

# Define the URL of the page with the list of equities
equities_url = "https://www.investing.com/equities/pakistan"

# Send a GET request to the server
try:
    response = requests.get(equities_url, headers={'User-Agent': 'Mozilla/5.0'})
    response.raise_for_status()  # Raise an HTTPError for bad responses
except requests.exceptions.RequestException as e:
    print(f"Error making the request: {e}")
    exit()

# Parse the HTML content of the page with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the equity links on the page
equity_links = soup.find_all('a', {'class': 'js-inner-all-results-quote-item row'})

# Print the full URL of each equity
for link in soup.find_all('a', href=True):
    equity_url = base_url + link['href'] + "-technical"
    print(equity_url)

