from concurrent.futures import ThreadPoolExecutor, as_completed, _base
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
import time
from pdb import set_trace
import os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd
class DataReader:

    headers = ['TIME','OPEN', 'HIGH', 'LOW','CLOSE','VOLUME']

    def __init__(self):
        self.__history = "https://dps.psx.com.pk/historical"
        self.__symbols = "https://dps.psx.com.pk/symbols"
        self.__dividends = "https://dps.psx.com.pk/screener"
        self.__local = threading.local()

    @property
    def session(self):
        if not hasattr(self.__local, "session"):
            self.__local.session = requests.Session()
        return self.__local.session

    def tickers(self):
        return pd.read_json(self.__symbols)

    def get_psx_data(self, symbol: str, dates: list) -> container:
        data = futures = []
        
        with tqdm(total=len(dates), desc="Downloading {}'s Data".format(symbol)) as progressbar:

            with ThreadPoolExecutor(max_workers=6) as executor:
                for date in dates:
                    futures.append(executor.submit(self.download, symbol=symbol, date=date))

                for future in as_completed(futures):
                    data.append(future.result())
                    progressbar.update(1)
            
            data = [instance for instance in data if isinstance(instance, container)]
        
        return self.preprocess(data)
    
    def stocks(self, tickers: Union[str, list], start: date, end: date) -> container:
        tickers = [tickers] if isinstance(tickers, str) else tickers
        dates = self.daterange(start, end)

        data = [self.get_psx_data(ticker, dates)[start: end] for ticker in tickers]

        if len(data) == 1:
            return data[0]

        return pd.concat(data, keys=tickers, names=["Ticker", "Date"])


    def download(self, symbol: str, date: date):
        session = self.session
        post = {"month": date.month, "year": date.year, "symbol": symbol}
        with session.post(self.__history, data=post) as response:
            data = parser(response.text, features="html.parser")
            data = self.toframe(data)
        return data

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

        for month in range(number_of_months):
            prev_date = dates[-1]
            dates.append(prev_date + relativedelta(months=1))

        dates = dates if len(dates) else [start]
        return dates
    
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

        # Evaluate each buy condition
            for condition in buy_conditions:
                if eval(condition, {}, {'row': row}):
                    conditions_met.append(condition)

        # Buy logic for each met condition
                    for met_condition in conditions_met:
                        if cash > row['Close']:
                            shares_bought = (cash - transaction_cost_per_share) // row['Close']
                            total_cost = shares_bought * row['Close'] + shares_bought * transaction_cost_per_share
                        if total_cost <= cash:
                            cash -= total_cost
                            shares += shares_bought
                            purchase_price_per_share = row['Close']
                    # Include met_condition in the trading log
                            trading_log.append((date, 'Buy', shares_bought, row['Close'], cash, shares, 0, met_condition))  # No P/L on buying

        # Sell logic
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
                            trading_log.append((date, 'Sell', shares, row['Close'], cash, 0, profit_loss, ''))  # No condition for selling

        print(f"Final Cash S4: {final_cash_out_S4}")
        print(f"Final Profit/Loss %: {(((final_cash_out_S4 - investment) / investment) * 100)}")
        return pd.DataFrame(trading_log, columns=['Date', 'Action', 'Shares', 'Price', 'Cash', 'Shares_Held', 'Profit_Loss', 'Condition'])

    # Add your is_dividend_date method and any other necessary methods here

    def preprocess(self, data: list) -> pd.DataFrame:
        # concatenate each frame to a single dataframe
        data = pd.concat(data)
        # sort the data by date
        data = data.sort_index()
        # change indexes from all uppercase to title
        data = data.rename(columns=str.title)
        # change index label Title to Date
        data.index.name = "Date"
        # remove non-numeric characters from volume column 
        data.Volume = data.Volume.str.replace(",", "")
        # coerce each column type to float
        for column in data.columns:
            data[column] = data[column].str.replace(",", "").astype(np.float64)
           
         # Calculate the Moving Average for Volume (e.g., 20-day)
        data['Volume_MA_20'] = data['Volume'].rolling(window=20).mean()
        # Calculate the percentage change in the 'Close' price
        data['Pct_Change'] = data['Close'].pct_change() * 100
        # Calculate daily fluctuation (High - Low)
        data['Daily_Fluctuation'] = data['High'] - data['Low']
        
        # Calculate the 30-day Moving Average for the 'Close' price
        data['MA_30'] = data['Close'].rolling(window=30).mean()

        # Existing RSI Calculations
        data['RSI_14'] = self.calculate_RSI(data, 14)
        data['RSI_9'] = self.calculate_RSI(data, 9)
        data['RSI_26'] = self.calculate_RSI(data, 26)

        data['RSI_14_Avg'] = data['RSI_14'].rolling(window=14).mean()
        # New RSI Calculations

        # Weekly RSI (Assuming 5 trading days in a week)
        data['RSI_Weekly'] = self.calculate_RSI(data, 5)

        # Monthly RSI (Approximately 21 trading days in a month)
        data['RSI_Monthly'] = self.calculate_RSI(data, 21)

        # Three-Monthly (Quarterly) RSI (Approximately 63 trading days in 3 months)
        data['RSI_3Months'] = self.calculate_RSI(data, 63)

        # Calculate AO
        data['AO'] = self.calculate_AO(data)
        # Calculate SMA of AO
        data['AO_SMA'] = data['AO'].rolling(window=5).mean()
        #final data
        return data   

data_reader = DataReader()

if __name__ == "__main__":
    # Get all symbols from PSX
        #symbols = data_reader.tickers()
        #get symbols from excel file nams psxsybbols.xlsx and save in symbols and sheet names kmiall
    symbols = pd.read_excel('psxsymbols.xlsx', sheet_name='MYLIST')
# Get the symbol names from the 'Symbol' column
    #symbols = symbols.iloc[:, 0].tolist()
    symbols = ['ACPL']
# Use the symbols in your code
years = 20  # User input for the number of years
start_date = date.today() - relativedelta(years=years)
end_date = date.today()

for symbol in symbols:
    print(f"Getting data for {symbol}")
            # Get the data for each symbol
    data = data_reader.stocks(symbol, start_date, end_date)
            # Simulate trading
    trading_log_S4 = data_reader.simulate_trading_S4(data)
            # Save the data to an excel file
            # Create a new file  in folder Strategy Analysis           
    folder_path = os.path.join(os.getcwd(), 'Strategy Analysis')
    file_path = os.path.join(folder_path, f"{symbol}-1.xlsx")
            # Delete the file if it already exists
    if os.path.exists(file_path):
        os.remove(file_path)
            # Create a new file
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            # Write each dataframe to a different worksheet
            data.to_excel(writer, sheet_name=f'{symbol}')
            # Write the trading log to a different worksheet
            trading_log_S4.to_excel(writer, sheet_name=f'{symbol}-Trading Log S4')
                # Save the file
               



      
       

    
