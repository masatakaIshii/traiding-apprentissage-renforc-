from datetime import timedelta
from tokenize import String
from typing import Optional

import pandas as pd

from logic.Stock import Stock
import yfinance as yf
from datetime import datetime


# Doit pendre en paramètre le nombre de catégorie qu'on veut
class FinanceService:
    start_date: str
    end_date: str

    def __init__(self, category_number: int = 5):
        self.__category_number = category_number
        self.__stock_history = pd.DataFrame()
        self.__current_interval = pd.DataFrame()
        self.__average_value = 0

    # call api so be careful to not use so much (one time maximum)
    def load_history(self, stock_name, start_date, end_date):
        self.start_date = start_date

        self.end_date = end_date
        ticker = yf.Ticker(stock_name)
        self.__stock_history = ticker.history(interval="1d", start=start_date, end=end_date)

    # def determine_categories(self):
    #     percentage_limit = 100 // self.__category_number
    #     self.__states = percentage_limit

    def get_stock(self, date: str, amount: float):
        stock_value = self.__stock_history.loc[date]['Close']
        if stock_value > 0:
            return Stock(date, amount, 100 * amount / stock_value)
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
        print(f"VALUE BY DATE : {value}")
        variation_percentage = self.get_variation_percentage_with_average(value)  # +50%
        print(f"VARIATION PERCENTAGE : {variation_percentage}")
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

    def set_stock_history(self, new_stock_history):
        self.__stock_history = new_stock_history

    @property
    def current_interval(self):
        return self.__current_interval

    def define_current_interval(self, start_date: str, days: int):
        start_date_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        # TODO Pb avec les dates ici, quoike
        end_date = start_date_datetime + timedelta(days=days)
        print(start_date)
        print(str(end_date))
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

    # def get_average_value_last_history_range(self, start_date, days):

    # def get_interval_one_stock_history(self, start_date: str, days: int):
    #     try:
    #         start_date_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    #         end_date = start_date_datetime + timedelta(days=days)
    #         return self.__stock_history.loc[start_date:end_date]
    #     except:
    #         return None

    def get_first_date_of_stock_history(self) -> str:
        return self.__stock_history.index[0]
