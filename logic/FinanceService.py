from datetime import timedelta
from typing import Optional

import pandas as pd

from bot.State import State
from logic.Stock import Stock
import yfinance as yf
from datetime import datetime


class FinanceService:
    def __init__(self):
        self.__stock_history = pd.DataFrame()
        self.__states = [State.VERY_LOW, State.LOW, State.LITTLE_LOW, State.LITTLE_HIGH, State.HIGH, State.VERY_HIGH]
        self.__average_value = 0

    # call api so be careful to not use so much (one time maximum)
    def load_history(self, stock_name, start_date, end_date):
        ticker = yf.Ticker(stock_name)
        self.__stock_history = ticker.history(interval="1d", start=start_date, end=end_date)
        self.__average_value = self.get_average_value()

    def get_stock(self, date: str, amount: float):
        stock_value = self.__stock_history.loc[date]['Close']
        if stock_value > 0:
            return Stock(date, amount, 100 * amount / stock_value)
        return Stock()

    def get_average_value(self) -> float:
        if len(self.__stock_history) < 1:
            return 0
        sum = 0
        for date, stock in self.__stock_history.iterrows():
            sum += stock['Close']
        return sum / len(self.__stock_history)

    def get_state_by_date(self, date: str) -> State:
        value = self.get_value_by_date(date)
        variation_percentage = self.get_variation_percentage(value)
        if 0 > variation_percentage >= -10:
            return State.LITTLE_LOW
        elif -10 > variation_percentage >= -30:
            return State.LOW
        elif variation_percentage < -30:
            return State.VERY_LOW
        elif 0 <= variation_percentage <= 10:
            return State.LITTLE_HIGH
        elif 10 < variation_percentage <= 30:
            return State.HIGH
        else:
            return State.VERY_HIGH

    def get_variation_percentage(self, value: float) -> float:
        if self.__average_value == value or self.__average_value == 0:
            return 0
        return (value - self.__average_value) / self.__average_value * 100

    @property
    def stock_history(self):
        return self.__stock_history

    @property
    def states(self):
        return self.__states

    def get_value_by_date(self, date: str) -> Optional[float]:
        return self.__stock_history.loc[date]['Close']

    def get_interval_one_stock_history(self, start_date, days):
        try:
            start_date_datetime = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = start_date_datetime + timedelta(days=days)
            return self.__stock_history.loc[start_date:end_date]['Close']
        except:
            return None
