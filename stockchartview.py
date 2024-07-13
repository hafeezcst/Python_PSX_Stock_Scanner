import os
import time
import datetime
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def capture_stock_charts(symbol):
    folder_path = "PSX_CHARTS"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    today_date = datetime.datetime.now().strftime("%B_%d_%Y")
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        urls = {
            'daily': f"https://www.tradingview.com/chart/?symbol=PSX%3A{symbol}&interval=D",
            'weekly': f"https://www.tradingview.com/chart/?symbol=PSX%3A{symbol}&interval=W",
            'monthly': f"https://www.tradingview.com/chart/?symbol=PSX%3A{symbol}&interval=M"
        }

        for interval, url in urls.items():
            try:
                driver.get(url)
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas')))
                screenshot_path = f'{folder_path}/{interval}_chart_{symbol}_{today_date}.png'
                driver.save_screenshot(screenshot_path)
                logging.info(f"{interval.capitalize()} chart for {symbol} saved to {screenshot_path}.")
                time.sleep(5)
            except Exception as e:
                logging.error(f"Error processing {symbol} for {interval} interval: {e}")
    finally:
        driver.quit()
        logging.info("Driver quit successfully.")

def capture_multiple_stock_charts(symbols):
    for symbol in symbols:
        logging.info(f"Capturing charts for {symbol}")
        capture_stock_charts(symbol)
        logging.info(f"Finished capturing charts for {symbol}")

# Example usage
symbols = ["OGDC"]  # Replace with any symbols you want to capture
capture_multiple_stock_charts(symbols)
