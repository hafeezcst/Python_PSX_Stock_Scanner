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
from sqlalchemy.orm import sessionmaker

class DataReader:
    headers = ['TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']

    def __init__(self, db_path='sqlite:///psx_data.db'):
        self.__history = "https://dps.psx.com.pk/historical"
        self.__symbols = "https://dps.psx.com.pk/symbols"
        self.__local = threading.local()
        self.engine = create_engine(db_path)
        self.metadata = MetaData()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    @property
    def requests_session(self):
        if not hasattr(self.__local, "session"):
            self.__local.session = requests.Session()
        return self.__local.session

    def tickers(self):
        try:
            return pd.read_json(self.__symbols)
        except Exception as e:
            print(f"Error fetching tickers: {e}")
            return pd.DataFrame()

    def get_psx_data(self, symbol: str, dates: list) -> container:
        data = []
        futures = []

        with tqdm(total=len(dates), desc=f"Downloading {symbol}'s Data") as progressbar:
            with ThreadPoolExecutor(max_workers=6) as executor:
                for date in dates:
                    futures.append(executor.submit(self.download, symbol=symbol, date=date))

                for future in as_completed(futures):
                    try:
                        result = future.result()
                        if isinstance(result, container):
                            data.append(result)
                    except Exception as e:
                        print(f"Error downloading data for {symbol} on {date}: {e}")
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
        session = self.requests_session
        post = {"month": date.month, "year": date.year, "symbol": symbol}
        try:
            with session.post(self.__history, data=post) as response:
                data = parser(response.text, features="html.parser")
                data = self.toframe(data)
            return data
        except Exception as e:
            print(f"Error downloading data for {symbol} on {date}: {e}")
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
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        RS = gain / loss
        RSI = 100 - (100 / (1 + RS))
        return RSI

    def calculate_AO(self, data):
        midpoint = (data['High'] + data['Low']) / 2
        SMA_short = midpoint.rolling(window=5).mean()
        SMA_long = midpoint.rolling(window=34).mean()
        AO = SMA_short - SMA_long
        return AO

    def simulate_trading_S4(self, data, investment=30000000, transaction_cost_per_share=0.00):
        cash = investment
        shares = 0
        trading_log = []
        purchase_price_per_share = 0
        final_cash_out_S4 = cash
        buy_conditions = [
            "row['RSI_14'] > 50",
            "row['RSI_14'] > 50 and row['AO'] > 0",
            "row['RSI_14'] > 50 and row['AO'] > 0 and row['Close'] > row['MA_30']",
            "row['RSI_14'] > row['RSI_14_Avg'] and row['AO'] > 0"
        ]

        for date, row in data.iterrows():
            conditions_met = []

            for condition in buy_conditions:
                if eval(condition, {}, {'row': row}):
                    conditions_met.append(condition)

            for met_condition in conditions_met:
                if cash > row['Close']:
                    shares_bought = (cash - transaction_cost_per_share) // row['Close']
                    total_cost = shares_bought * row['Close'] + shares_bought * transaction_cost_per_share
                    if total_cost <= cash:
                        cash -= total_cost
                        shares += shares_bought
                        purchase_price_per_share = row['Close']
                        trading_log.append((date, 'Buy', shares_bought, row['Close'], cash, shares, 0, met_condition))

                if shares > 0:
                    current_price = row['Close']
                    profit_loss_per_share = current_price - purchase_price_per_share
                    profit_loss_percent = (profit_loss_per_share / purchase_price_per_share) * 100

                    if profit_loss_percent > 20 or profit_loss_percent < -10:
                        total_proceeds = shares * current_price
                        transaction_costs = shares * transaction_cost_per_share
                        profit_loss = total_proceeds - (shares * purchase_price_per_share) - transaction_costs
                        cash += total_proceeds - transaction_costs
                        final_cash_out_S4 = cash
                        trading_log.append((date, 'Sell', shares, row['Close'], cash, 0, profit_loss, ''))

        print(f"Final Cash S4: {final_cash_out_S4}")
        print(f"Final Profit/Loss %: {(((final_cash_out_S4 - investment) / investment) * 100)}")
        return pd.DataFrame(trading_log, columns=['Date', 'Action', 'Shares', 'Price', 'Cash', 'Shares_Held', 'Profit_Loss', 'Condition'])

    def preprocess(self, data: list) -> pd.DataFrame:
        data = pd.concat(data)
        data = data.sort_index()
        data = data.rename(columns=str.title)
        data.index.name = "Date"
        data.Volume = data.Volume.str.replace(",", "").astype(np.float64)
        for column in data.columns:
            data[column] = data[column].str.replace(",", "").astype(np.float64)

        data['Volume_MA_20'] = data['Volume'].rolling(window=20).mean()
        data['Pct_Change'] = data['Close'].pct_change() * 100
        data['Daily_Fluctuation'] = data['High'] - data['Low']
        data['MA_30'] = data['Close'].rolling(window=30).mean()
        data['RSI_14'] = self.calculate_RSI(data, 14)
        data['RSI_9'] = self.calculate_RSI(data, 9)
        data['RSI_26'] = self.calculate_RSI(data, 26)
        data['RSI_14_Avg'] = data['RSI_14'].rolling(window=14).mean()
        data['RSI_Weekly'] = self.calculate_RSI(data, 5)
        data['RSI_Monthly'] = self.calculate_RSI(data, 21)
        data['RSI_3Months'] = self.calculate_RSI(data, 63)
        data['AO'] = self.calculate_AO(data)
        data['AO_SMA'] = data['AO'].rolling(window=5).mean()

        return data

    def save_to_db(self, data: pd.DataFrame, table_name: str):
        # Batch insert data to the database
        data.to_sql(table_name, self.engine, if_exists='append', index=True, chunksize=1000)

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

    for symbol in symbols:
        print(f"Getting data for {symbol}")
        try:
            data = data_reader.stocks(symbol, start_date, end_date)
            trading_log_S4 = data_reader.simulate_trading_S4(data)
            data_reader.save_to_db(data, f'{symbol}_data')
            data_reader.save_to_db(trading_log_S4, f'{symbol}_trading_log')
            file_path = os.path.join(folder_path, f"{symbol}.xlsx")
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                data.to_excel(writer, sheet_name=f'{symbol}')
                trading_log_S4.to_excel(writer, sheet_name=f'{symbol}-Trading Log S4')
        except Exception as e:
            print(f"Error processing data for {symbol}: {e}")
