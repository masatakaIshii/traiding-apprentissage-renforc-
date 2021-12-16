from datetime import date
from typing import Optional

from logic.FinanceService import FinanceService
from logic.Stock import Stock
from logic.Wallet import Wallet
from logic.exceptions.IncorrectBuyAmountError import IncorrectBuyAmountError


class WalletService:
    def __init__(self, wallet: Wallet, finance_service: FinanceService):
        self.__wallet = wallet
        self.__finance_service = finance_service

    def get_amount(self):
        return self.__wallet.wallet_amount

    def buy_stock(self, cur_date_str: str, amount: float) -> Stock:
        stock_to_buy = self.__finance_service.get_stock(cur_date_str, amount)

        stock_total_cost = stock_to_buy.purchase_value * (stock_to_buy.share_percentage / 100)
        if self.__wallet.wallet_amount - stock_total_cost < 0:
            raise IncorrectBuyAmountError
        self.__wallet.wallet_amount -= stock_total_cost
        self.__wallet.stocks.append(stock_to_buy)

        return stock_to_buy

    def get_stocks(self) -> [Stock]:
        return self.__wallet.stocks

    def get_stock(self, index: int) -> Optional[Stock]:
        stocks = self.__wallet.stocks
        if len(stocks) == index:
            return None
        return stocks[index]

    def sell_stock(self, index: int, cur_date_str = date.today().strftime('%m-%d-%Y')):
        stocks = self.__wallet.stocks
        stock_to_sell = self.__finance_service.get_stock(cur_date_str, stocks[index].purchase_value)

        cur_stock_total_cost = stock_to_sell.purchase_value * (stock_to_sell.share_percentage / 100)
        stock_total_cost = stocks[index].purchase_value * (stocks[index].share_percentage / 100)

        plus_value = cur_stock_total_cost - stock_total_cost
        self.__wallet.wallet_amount += cur_stock_total_cost - (plus_value * 0.3)
        self.__wallet.stocks.remove(stocks[index])
        pass
