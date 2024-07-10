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
import pandas as pd

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def capture_stock_charts(symbol):
    folder_path = "PSX_CHARTS"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    today_date = datetime.datetime.now().strftime("%B %d, %Y")
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        urls = {
            'daily'     : f"https://www.tradingview.com/chart/?symbol=PSX%3A{symbol}&interval=D",
            'weekly'    : f"https://www.tradingview.com/chart/?symbol=PSX%3A{symbol}&interval=W",
            'monthly'   : f"https://www.tradingview.com/chart/?symbol=PSX%3A{symbol}&interval=M"
            #'3monthly'  : f":https://www.tradingview.com/chart/?symbol=PSX%3A{symbol}&interval=3M",
            #'6monthly'  : f":https://www.tradingview.com/chart/?symbol=PSX%3A{symbol}&interval=6M"
        }

        for interval, url in urls.items():
            try:
                driver.get(url)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                screenshot_path = f'{folder_path}/{interval}_chart_{symbol}_{today_date}.png'
                driver.save_screenshot(screenshot_path)
                logging.info(f"{interval.capitalize()} chart for {symbol} saved.")
                time.sleep(5)
            except Exception as e:
                logging.error(f"Error processing {symbol} for {interval}: {e}")

    finally:
        driver.quit()
        logging.info("Driver quit successfully.")

# Example usage
#capture_stock_charts("OGDC")  # Replace "OGDC" with any symbol you want to capture
