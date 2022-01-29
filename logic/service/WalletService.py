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

    # amount is in dollar
    def buy_stock(self, cur_date_str: str, amount: float) -> Stock:
        stock_to_buy = self.__finance_service.get_stock(cur_date_str, amount)

        if self.__wallet.wallet_amount - amount <= 0:
            raise IncorrectBuyAmountError
        # self.__wallet.last_wallet_amount = self.__wallet.wallet_amount
        self.__wallet.wallet_amount -= amount
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
        stocks = self.__wallet.stocks
        stock_to_sell: Stock = stocks.pop(index)

        cur_value = self.__finance_service.get_value_by_date(cur_date_str)
        if cur_value is None:
            raise StockNotFoundError

        cur_amount_value = cur_value * stock_to_sell.share_percentage / 100
        stock_to_sell_amount_value = stock_to_sell.purchase_value * stock_to_sell.share_percentage / 100
        profit: float = cur_amount_value - stock_to_sell_amount_value

        # self.__wallet.last_wallet_amount = self.__wallet.wallet_amount
        self.__wallet.wallet_amount = self.__wallet.wallet_amount + cur_amount_value

        if profit > 0:
            bill_percent_on_profit = 0.3
            self.__wallet.wallet_amount -= profit * bill_percent_on_profit

            # profit -= profit * bill_percent_on_profit

        # return ((initial_value / self.__wallet.wallet_amount) - 1) * 100  # pour avoir le pourcentage

    @property
    def finance_service(self):
        return self.__finance_service

    # def get_profit_percentage(self) -> float:
    #     # Formule du taux de variation
    #     if self.__wallet.wallet_amount == self.__wallet.initial_value:
    #         return 0
    #     return (self.__wallet.wallet_amount - self.__wallet.initial_value) / self.__wallet.initial_value * 100

    def can_buy_stock(self, amount: float) -> bool:
        return len(self.__wallet.stocks) <= 0 and self.__wallet.wallet_amount > amount

    def contains_stock(self) -> bool:
        return len(self.__wallet.stocks) > 0

    def get_potentiel_total_amount(self, current_date: str) -> float:
        percentage_stock_possess = sum(stock.share_percentage for stock in self.__wallet.stocks)

        current_stock_value = self.__finance_service.get_value_by_date(current_date)
        return self.__wallet.wallet_amount + (percentage_stock_possess / 100 * current_stock_value)

    def get_last_action_profit_percentage(self, current_date: str) -> float:
        total_virtual_value = self.get_potentiel_total_amount(current_date)
        # print(f"TOTAL VIRTUAL VALUE {total_virtual_value}")
        if total_virtual_value == self.__wallet.last_wallet_amount:
            return 0
        return (total_virtual_value - self.__wallet.last_wallet_amount) / self.__wallet.last_wallet_amount * 100

    # def keep_stock(self, current_date: str):
    #     self.__wallet.last_wallet_amount = self.get_potentiel_total_amount(current_date)

    def get_potential_amount(self, cur_date_str: str) -> float:
        if len(self.__wallet.stocks) > 0:
            stock = self.__wallet.stocks[0]
            current_date_value = self.__finance_service.get_value_by_date(cur_date_str)
            # print(f"CURRENT VALUE : {current_date_value} DONC POT AMOUNT {self.__wallet.wallet_amount + current_date_value * stock.share_percentage / 100}")
            return self.__wallet.wallet_amount + current_date_value * stock.share_percentage / 100
        return self.__wallet.wallet_amount

    def reset(self):
        self.__wallet = Wallet()

    def update_last_amount(self, current_date: str):
        # print(f"POTENTIAL VALUE {self.get_potentiel_total_amount(current_date)}")
        self.__wallet.last_wallet_amount = self.get_potentiel_total_amount(current_date)

    def get_variation_with_average(self, cur_date_str: str):
        average_value = self.__finance_service.average_value
        current_value = self.__finance_service.get_value_by_date(cur_date_str)
        # print(f"DATE VALUE : {current_value}")
        # print(f"AVERAGE VALUE : {average_value}")
        return self.__finance_service.get_variation_percentage(current_value, average_value)
