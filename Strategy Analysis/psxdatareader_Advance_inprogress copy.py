import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from dateutil.relativedelta import relativedelta
from pandas import DataFrame as container
from bs4 import BeautifulSoup as parser
from collections import defaultdict
from datetime import datetime, date
from typing import Union
from tqdm import tqdm
import threading
import pandas as pd
import numpy as np
import requests
import os
from sqlalchemy import create_engine, MetaData

logging.basicConfig(filename='data_reader.log', level=logging.ERROR)

class DataReader:
    headers = ['TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']

    def __init__(self, db_path='sqlite:///psx_data.db'):
        self.__history = "https://dps.psx.com.pk/historical"
        self.__symbols = "https://dps.psx.com.pk/symbols"
        self.__local = threading.local()
        self.engine = create_engine(db_path)
        self.metadata = MetaData()
        self.max_workers = min(32, os.cpu_count() + 4)

    @property
    def session(self):
        if not hasattr(self.__local, "session"):
            self.__local.session = requests.Session()
        return self.__local.session

    def tickers(self):
        try:
            return pd.read_json(self.__symbols)
        except Exception as e:
            logging.error(f"Error fetching tickers: {e}")
            return pd.DataFrame()

    def get_psx_data(self, symbol: str, dates: list) -> container:
        data = []
        futures = []

        with tqdm(total=len(dates), desc=f"Downloading {symbol}'s Data") as progressbar:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                for date in dates:
                    futures.append(executor.submit(self.download, symbol=symbol, date=date))

                for future in as_completed(futures):
                    try:
                        result = future.result()
                        if isinstance(result, container):
                            data.append(result)
                    except Exception as e:
                        logging.error(f"Error downloading data for {symbol} on {date}: {e}")
                    progressbar.update(1)

        return self.preprocess(data)

    def stocks(self, tickers: Union[str, list], start: date, end: date) -> container:
        tickers = [tickers] if isinstance(tickers, str) else tickers
        dates = self.daterange(start, end)
        data = [self.get_psx_data(ticker, dates) for ticker in tickers]

        if len(data) == 1:
            return data[0]

        return pd.concat(data, keys=tickers, names=["Ticker", "Date"])

    def download(self, symbol: str, date: date):
        session = self.session
        post = {"month": date.month, "year": date.year, "symbol": symbol}
        try:
            with session.post(self.__history, data=post) as response:
                data = parser(response.text, features="html.parser")
                data = self.toframe(data)
            return data
        except Exception as e:
            logging.error(f"Error downloading data for {symbol} on {date}: {e}")
            return pd.DataFrame()

    def toframe(self, data):
        stocks = defaultdict(list)
        rows = data.select("tr")

        for row in rows:
            cols = [col.getText() for col in row.select("td")]
            for key, value in zip(self.headers, cols):
                if key == "TIME":
                    value = datetime.strptime(value, "%b %d, %Y")
                stocks[key].append(value)

        return pd.DataFrame(stocks, columns=self.headers).set_index("TIME")

    def daterange(self, start: date, end: date) -> list:
        period = end - start
        number_of_months = period.days // 30
        current_date = datetime(start.year, start.month, 1)
        dates = [current_date]

        for _ in range(number_of_months):
            prev_date = dates[-1]
            dates.append(prev_date + relativedelta(months=1))

        return dates if len(dates) else [start]

    def calculate_RSI(self, data, period=14):
        """
        Calculate the Relative Strength Index (RSI) for a given data frame.

        Parameters:
        data (DataFrame): The input data containing stock prices.
        period (int): The period over which to calculate the RSI.

        Returns:
        Series: The RSI values.
        """
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        RS = gain / loss
        RSI = 100 - (100 / (1 + RS))
        return RSI

    def calculate_AO(self, data):
        """
        Calculate the Awesome Oscillator (AO) for a given data frame.

        Parameters:
        data (DataFrame): The input data containing stock prices.

        Returns:
        Series: The AO values.
        """
        midpoint = (data['High'] + data['Low']) / 2
        SMA_short = midpoint.rolling(window=5).mean()
        SMA_long = midpoint.rolling(window=34).mean()
        AO = SMA_short - SMA_long
        return AO

    def simulate_trading_S4(self, data, investment=30000000, transaction_cost_per_share=0.00, buy_condition="row['RSI_14'] > 40", sell_condition="row['RSI_14'] < 50"):
        """
        Simulate a trading strategy based on RSI and AO indicators.

        Parameters:
        data (DataFrame): The input data containing stock prices and indicators.
        investment (float): The initial investment amount.
        transaction_cost_per_share (float): The transaction cost per share.
        buy_condition (str): The condition to buy shares.
        sell_condition (str): The condition to sell shares.

        Returns:
        DataFrame: The trading log containing details of each transaction.
        """
        cash = investment
        shares = 0
        trading_log = []
        purchase_price_per_share = 0
        final_cash_out_S4 = cash

        for date, row in data.iterrows():
            try:
                # Buy logic
                if eval(buy_condition, {}, {'row': row}) and cash > row['Close']:
                    shares_bought = (cash - transaction_cost_per_share) // row['Close']
                    total_cost = shares_bought * row['Close'] + shares_bought * transaction_cost_per_share
                    if total_cost <= cash:
                        cash -= total_cost
                        shares += shares_bought
                        purchase_price_per_share = row['Close']
                        trading_log.append((date, 'Buy', shares_bought, row['Close'], cash, shares, 0, buy_condition))

                # Sell logic
                if shares > 0:
                    current_price = row['Close']
                    profit_loss_per_share = current_price - purchase_price_per_share
                    profit_loss_percent = (profit_loss_per_share / purchase_price_per_share) * 100

                    if eval(sell_condition, {}, {'row': row}) or profit_loss_percent > 20 or profit_loss_percent < -10:
                        total_proceeds = shares * current_price
                        transaction_costs = shares * transaction_cost_per_share
                        profit_loss = total_proceeds - (shares * purchase_price_per_share) - transaction_costs
                        cash += total_proceeds - transaction_costs
                        final_cash_out_S4 = cash
                        trading_log.append((date, 'Sell', shares, row['Close'], cash, 0, profit_loss, sell_condition))

            except Exception as e:
                logging.error(f"Error processing trade on {date}: {e}")

        print(f"Final Cash S4: {final_cash_out_S4}")
        print(f"Final Profit/Loss %: {(((final_cash_out_S4 - investment) / investment) * 100)}")
        return pd.DataFrame(trading_log, columns=['Date', 'Action', 'Shares', 'Price', 'Cash', 'Shares_Held', 'Profit_Loss', 'Condition'])

    def preprocess(self, data: list) -> pd.DataFrame:
        """
        Preprocess the stock data by cleaning and calculating various indicators.

        Parameters:
        data (list): List of data frames containing stock data.

        Returns:
        DataFrame: The processed data frame with additional indicators.
        """
        data = pd.concat(data)
        data = data.sort_index()
        data = data.rename(columns=str.title)
        data.index.name = "Date"
        data.Volume = data.Volume.str.replace(",", "")
        for column in data.columns:
            data[column] = data[column].str.replace(",", "").astype(np.float64)

        data['Volume_MA_20'] = data['Volume'].rolling(window=20).mean() # 20-day moving average
        data['Pct_Change'] = data['Close'].pct_change() * 100 # Daily percentage change
        data['Daily_Fluctuation'] = data['High'] - data['Low'] # Daily fluctuation
        data['MA_30'] = data['Close'].rolling(window=30).mean()     # 30-day moving average
        data['RSI_14'] = self.calculate_RSI(data, 14) # 14-day RSI
        data['RSI_9'] = self.calculate_RSI(data, 9) # 9-day RSI
        data['RSI_26'] = self.calculate_RSI(data, 26) # 26-day RSI
        data['RSI_14_Avg'] = data['RSI_14'].rolling(window=14).mean() # 14-day RSI average
        data['RSI_Weekly'] = self.calculate_RSI(data, 5) # weekly  RSI
        data['RSI_Weekly_Avg'] = data['RSI_Weekly'].rolling(window=5).mean() # weekly  RSI average
        data['RSI_Monthly'] = self.calculate_RSI(data, 21) # monthly  RSI
        data['RSI_Monthly_Avg'] = data['RSI_Monthly'].rolling(window=21).mean() # monthly  RSI average
        data['RSI_3Months'] = self.calculate_RSI(data, 63)  # 3-month RSI
        data['RSI_3Months_Avg'] = data['RSI_3Months'].rolling(window=63).mean() # 3-month RSI average
        data['AO'] = self.calculate_AO(data)     # Awesome Oscillator
        data['AO_MA'] = data['AO'].rolling(window=5).mean() # 5-day moving average of AO
        data['AO_SMA'] = data['AO'].rolling(window=5).mean() # 5-day moving average of AO

        return data

    def save_to_db(self, data: pd.DataFrame, table_name: str):
        """
        Save the processed data to a SQLite database.

        Parameters:
        data (DataFrame): The data frame to be saved.
        table_name (str): The name of the table to save the data in.
        """
        data.to_sql(table_name, self.engine, if_exists='append', index=True)

data_reader = DataReader()

if __name__ == "__main__":
    symbols = pd.read_excel('psxsymbols.xlsx', sheet_name='KMIALL')
    symbols = symbols.iloc[:, 0]
    years = 20
    start_date = date.today() - relativedelta(years=years)
    end_date = date.today()

    folder_path = os.path.join(os.getcwd(), 'Strategy Analysis')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    buy_conditions = [
        "row['RSI_14'] > 40",
        "row['AO'] > 0",
        "row['RSI_14'] > 40 and row['AO'] > 0",
        "row['RSI_14'] > row['RSI_14_Avg']",
        "row['RSI_Weekly'] > 40",
        "row['RSI_Weekly'] > 40 and row['AO'] > 0",
        "row['RSI_Weekly'] > row['RSI_Weekly_Avg']",
        "row['RSI_Monthly'] > 40",
        "row['RSI_Monthly'] > 40 and row['AO'] > 0",
        "row['RSI_Monthly'] > row['RSI_Monthly_Avg']",
    ]

    sell_conditions = [
        "row['RSI_14'] < 50",
        "row['AO'] < 0",
        "row['RSI_14'] < 40 and row['AO'] < 0",
        "row['RSI_14'] < row['RSI_14_Avg']",
        "row['RSI_Weekly'] < 40",
        "row['RSI_Weekly']< 40 and row['AO'] < 0",
        "row['RSI_Weekly'] < row['RSI_Weekly_Avg']",
        "row['RSI_Monthly'] < 40",
        "row['RSI_Monthly'] < 40 and row['AO'] < 0",
        "row['RSI_Monthly'] < row['RSI_Monthly_Avg']",
    ]

    for symbol in symbols:
        print(f"Getting data for {symbol}")
        try:
            data = data_reader.stocks(symbol, start_date, end_date)
            for buy_condition in buy_conditions:
                for sell_condition in sell_conditions:
                    trading_log_S4 = data_reader.simulate_trading_S4(data, buy_condition=buy_condition, sell_condition=sell_condition)
                    data_reader.save_to_db(data, f'{symbol}_data')
                    data_reader.save_to_db(trading_log_S4, f'{symbol}_trading_log')
                    buy_condition_name = buy_condition.replace(" ", "_").replace("'", "").replace("[", "").replace("]", "").replace(">", "gt").replace("<", "lt")
                    sell_condition_name = sell_condition.replace(" ", "_").replace("'", "").replace("[", "").replace("]", "").replace(">", "gt").replace("<", "lt")
                    file_path = os.path.join(folder_path, f"{symbol}-Buy_{buy_condition_name}-Sell_{sell_condition_name}.xlsx")
                    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                        data.to_excel(writer, sheet_name=f'{symbol}')
                        trading_log_S4.to_excel(writer, sheet_name=f'{symbol}-Trading Log S4')
        except Exception as e:
            logging.error(f"Error processing data for {symbol}: {e}")
