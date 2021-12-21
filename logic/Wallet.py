# Récupérer les infos entre deux dates
# Sauvegarder le paquetol
# Faire les calculs au moment de l'achat / vente etc
from logic.FinanceService import FinanceService
from logic.Stock import Stock
from logic.exceptions.IncorrectBuyAmountError import IncorrectBuyAmountError


class Wallet:
    def __init__(self, wallet_amount=100):
        self.__wallet_amount: float = wallet_amount
        self.__stocks: [Stock] = []

    def buy(self, stock_name, amount):
        if amount > self.__wallet_amount:
            raise IncorrectBuyAmountError

        self.__wallet_amount -= amount

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

