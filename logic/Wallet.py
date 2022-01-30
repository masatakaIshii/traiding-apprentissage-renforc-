from logic.Stock import Stock
from logic.exceptions.IncorrectBuyAmountError import IncorrectBuyAmountError


class Wallet:
    def __init__(self, wallet_amount=5000):
        self.__wallet_amount: float = wallet_amount
        self.__last_wallet_amount: float = wallet_amount
        self.__initial_value: float = wallet_amount
        self.__stocks: [Stock] = []

    def buy(self, amount):
        if amount > self.__wallet_amount:
            raise IncorrectBuyAmountError

        self.__wallet_amount -= amount

    @property
    def last_wallet_amount(self) -> float:
        return self.__last_wallet_amount

    @last_wallet_amount.setter
    def last_wallet_amount(self, amount: float):
        self.__last_wallet_amount = amount

    @property
    def initial_value(self) -> float:
        return self.__initial_value

    @property
    def wallet_amount(self):
        return self.__wallet_amount

    @property
    def stocks(self) -> [Stock]:
        return self.__stocks

    @wallet_amount.setter
    def wallet_amount(self, value):
        self.__wallet_amount = value

    @stocks.setter
    def stocks(self, value: [Stock]):
        self.__stocks = value

    def __str__(self) -> str:
        return f"Wallet(wallet_amount={self.__wallet_amount}, stocks={self.__stocks})"
