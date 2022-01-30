from datetime import timedelta
from tokenize import String
from typing import Optional

import pandas as pd
from pandas import DataFrame

from logic.Stock import Stock
import yfinance as yf
from datetime import datetime


# Doit pendre en paramètre le nombre de catégorie qu'on veut
class FinanceService:
    stock_name: str
    start_date: str
    end_date: str

    def __init__(self, category_number: int = 5):
        self.__category_number = category_number
        self.__stock_history = pd.DataFrame()
        self.__current_interval = pd.DataFrame()
        self.__average_value = 0

    @property
    def average_value(self) -> float:
        return self.__average_value

    # call api so be careful to not use so much (one time maximum)
    def load_history(self, stock_name, start_date, end_date):
        ticker = yf.Ticker(stock_name)
        fetched_history = ticker.history(interval="1d", start=start_date, end=end_date)

        if len(fetched_history) <= 0:
            return False
        self.__stock_history = fetched_history
        self.stock_name = stock_name
        self.start_date = start_date
        self.end_date = end_date
        return True

    def get_stock(self, date: str):
        stock_value = self.__stock_history.loc[date]['Close']
        if stock_value > 0:
            return Stock(date, stock_value)
        return Stock()

    def get_average_value(self) -> float:
        if len(self.__current_interval) < 1:
            return 0
        sum = 0
        for date, stock in self.__current_interval.iterrows():
            sum += stock['Close']
        return sum / len(self.__current_interval)

    def get_state_by_date(self, date: str) -> int:
        value = self.get_value_by_date(date)  # 3$ avec une moyenne des deux semaines préc. à 2$
        # print(f"VALUE BY DATE : {value}")
        variation_percentage = self.get_variation_percentage_with_average(value)  # +50%
        # print(f"VARIATION PERCENTAGE : {variation_percentage}")
        return self.determine_state_by_value(variation_percentage)

    def determine_state_by_value(self, value: float) -> int:
        if value < -50:
            return 0
        cur_value = -50
        for i in range(self.__category_number):
            superior_limit = cur_value + 100 // self.__category_number
            if cur_value <= value <= superior_limit:
                return i
            cur_value = superior_limit
        return self.__category_number - 1

    def get_variation_percentage_with_average(self, value: float) -> float:
        return self.get_variation_percentage(value, self.__average_value)

    def get_variation_percentage(self, value: float, precedent_value: float) -> float:
        if precedent_value == value or precedent_value == 0:
            return 0
        return (value - precedent_value) / precedent_value * 100

    @property
    def stock_history(self):
        return self.__stock_history

    def set_stock_history(self, new_stock_history: DataFrame, stock_name: str = 'Default'):
        self.__stock_history = new_stock_history
        date_indexes = new_stock_history.index
        self.start_date = date_indexes[0]
        self.end_date = date_indexes[len(date_indexes) - 1]
        self.stock_name = stock_name

    @property
    def current_interval(self):
        return self.__current_interval

    def define_current_interval(self, start_date: str, days: int):
        start_date_datetime = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        end_date = start_date_datetime + timedelta(days=days)
        self.__current_interval = self.__stock_history.loc[start_date:str(end_date)]
        self.__average_value = self.get_average_value()

    @property
    def category_number(self) -> int:
        return self.__category_number

    def get_value_by_date(self, date: str) -> Optional[float]:
        return self.__stock_history.loc[date]['Close']

    def next_date(self, date: str) -> str:
        date_reach = False
        for idx, value in self.__stock_history.iterrows():
            if date_reach:
                return str(idx)
            if str(idx) == date:
                date_reach = True
        return ""

    def get_first_date_of_stock_history(self) -> str:
        return self.__stock_history.index[0]

    @category_number.setter
    def category_number(self, value: int):
        self.__category_number = value
