from datetime import date
from typing import Optional

from logic.FinanceService import FinanceService
from logic.Stock import Stock
from logic.Wallet import Wallet
from logic.exceptions.IncorrectBuyAmountError import IncorrectBuyAmountError
from logic.exceptions.StockNotFoundError import StockNotFoundError


class WalletService:
    def __init__(self, wallet: Wallet, finance_service: FinanceService):
        self.__wallet = wallet
        self.__finance_service = finance_service

    def get_amount(self):
        return self.__wallet.wallet_amount

    def buy_stock(self, cur_date_str: str) -> Stock:
        stock_to_buy = self.__finance_service.get_stock(cur_date_str)

        if self.__wallet.wallet_amount - stock_to_buy.purchase_value <= 0:
            raise IncorrectBuyAmountError

        self.__wallet.wallet_amount -= stock_to_buy.purchase_value
        self.__wallet.stocks.append(stock_to_buy)

        return stock_to_buy

    def get_stocks(self) -> [Stock]:
        return self.__wallet.stocks

    def get_stock(self, index: int) -> Optional[Stock]:
        stocks = self.__wallet.stocks
        if len(stocks) == index:
            return None
        return stocks[index]

    def sell_stock_and_return_profit(self, index: int, cur_date_str=date.today().strftime('%m-%d-%Y')):
        self.__wallet.stocks.pop(index)

        cur_value = self.__finance_service.get_value_by_date(cur_date_str)
        if cur_value is None:
            raise StockNotFoundError

        self.__wallet.wallet_amount = self.__wallet.wallet_amount + cur_value

    @property
    def finance_service(self):
        return self.__finance_service

    def can_buy_stock(self, amount: float) -> bool:
        return len(self.__wallet.stocks) <= 0 and self.__wallet.wallet_amount > amount

    def contains_stock(self) -> bool:
        return len(self.__wallet.stocks) > 0

    def get_potential_amount(self, cur_date_str: str) -> float:
        current_date_value = self.__finance_service.get_value_by_date(cur_date_str)
        return self.__wallet.wallet_amount + current_date_value * len(self.__wallet.stocks)

    def reset(self):
        self.__wallet = Wallet()

    def get_variation_with_average(self, cur_date_str: str):
        average_value = self.__finance_service.average_value
        current_value = self.__finance_service.get_value_by_date(cur_date_str)

        return self.__finance_service.get_variation_percentage(current_value, average_value)
