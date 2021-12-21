from typing import Optional

import pandas as pd
from logic.Stock import Stock
import yfinance as yf


class FinanceService:
    def __init__(self):
        self.__stock_history = pd.DataFrame()

    # call api so be careful to not use so much (one time maximum)
    def load_history(self, stock_name, start_date, end_date):
        ticker = yf.Ticker(stock_name)
        self.__stock_history = ticker.history(interval="1d", start=start_date, end=end_date)

    def get_stock(self, date: str, amount: float):
        stock_value = self.__stock_history.loc[date]['Close']
        if stock_value > 0:
            return Stock(date, amount, round(100 * amount / stock_value, 2))
        return Stock()

    @property
    def stock_history(self):
        return self.__stock_history

    def get_value_by_date(self, date: str) -> Optional[float]:
        return self.__stock_history.loc[date]['Close']

    # TODO : for Jerem and use TDD mandatory
    def get_interval_one_stock_history(self, start_date, end_date):
        pass
