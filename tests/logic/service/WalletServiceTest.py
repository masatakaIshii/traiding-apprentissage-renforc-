import unittest
from datetime import date
from unittest.mock import MagicMock

from logic.Stock import Stock
from logic.Wallet import Wallet
from logic.exceptions.IncorrectBuyAmountError import IncorrectBuyAmountError
from logic.exceptions.StockNotFoundError import StockNotFoundError
from logic.service.WalletService import WalletService


class WalletServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_finance_service = MagicMock()
        self.wallet = Wallet()
        self.wallet_service = WalletService(self.wallet, self.mock_finance_service)

    def test_get_amount_should_return_amount_of_wallet(self):
        wallet_amount = 33
        self.wallet.wallet_amount = wallet_amount

        self.assertEqual(wallet_amount, self.wallet_service.get_amount())

    def test_buy_stock_should_reduce_amount_of_wallet_depend_to_found_stock(self):
        today_str = date.today().strftime('%m-%d-%Y')
        purchase_value = 36
        share_percentage = 50
        self.mock_finance_service.get_stock.return_value = Stock(today_str, purchase_value, share_percentage)
        wallet_amount = self.wallet.wallet_amount
        self.assertEqual(100, wallet_amount)
        self.wallet_service.buy_stock(today_str, share_percentage)

        self.assertEqual(50, self.wallet.wallet_amount)

    def test_buy_stock_after_bought_stock_should_add_in_wallet(self):
        today = date.today().strftime('%m-%d-%Y')
        purchase_value = 36
        share_percentage = 50
        self.mock_finance_service.get_stock.return_value = Stock(today, purchase_value, share_percentage)

        len_stock = len(self.wallet.stocks)

        self.wallet_service.buy_stock(today, share_percentage)

        self.assertEqual(len_stock + 1, len(self.wallet.stocks))

    def test_buy_stock_after_add_bought_stock_should_return_bought_stock(self):
        today = date.today().strftime('%m-%d-%Y')
        purchase_value = 36
        share_percentage = 50
        expected_stock = Stock(today, purchase_value, share_percentage)
        self.mock_finance_service.get_stock.return_value = expected_stock

        result = self.wallet_service.buy_stock(today, share_percentage)

        self.assertEqual(expected_stock, result)

    def test_buy_stock_after_and_wallet_not_have_enough_money_should_raises_exception(self):
        purchase_value = 100
        share_percentage = 100.1
        today = date.today().strftime('%m-%d-%Y')
        expected_stock = Stock(today, purchase_value, share_percentage)
        self.mock_finance_service.get_stock.return_value = expected_stock

        with self.assertRaises(IncorrectBuyAmountError):
            self.wallet_service.buy_stock(today, share_percentage)

    def test_get_stocks_should_return_all_stocks_on_wallet(self):
        self.wallet.stocks = stocks = [
            Stock("20-10-2020", 5, 4)
        ]

        result = self.wallet_service.get_stocks()

        self.assertEqual(result, stocks)

    def test_get_stock_should_get_one_stock_based_on_stocks_by_index(self):
        expect_stock = Stock("20-10-2020", 5, 4)
        self.wallet.stocks = [
            expect_stock
        ]

        result = self.wallet_service.get_stock(0)

        self.assertEqual(result, expect_stock)

    def test_get_stock_should_return_none_when_index_equal_than_len_of_stocks(self):
        expect_stock = Stock("20-10-2020", 5, 4)
        stocks = [
            expect_stock
        ]
        self.wallet.stocks = stocks

        cur_index = 1

        result = self.wallet_service.get_stock(cur_index)

        self.assertEqual(len(stocks), cur_index)
        self.assertIsNone(result)

    def test_sell_stock_and_return_profit_when_finance_service_return_none_should_raise_exception(self):
        expect_stock = Stock("20-10-2020", 5, 4)
        type(self.wallet).stocks = [
            expect_stock
        ]
        today = date.today().strftime('%m-%d-%Y')
        self.mock_finance_service.get_value_by_date.return_value = None

        with self.assertRaises(StockNotFoundError):
            self.wallet_service.sell_stock_and_return_profit(0, today)

    def test_sell_stock_and_return_profit_when_got_value_by_current_date_of_finance_service_should_add_wallet_amount(
            self):
        expect_stock = Stock(
            purchase_date="20-10-2020",
            purchase_value=100,
            share_percentage=50)
        self.wallet.stocks = [
            expect_stock
        ]
        before_sell_wallet_amount = self.wallet.wallet_amount
        self.mock_finance_service.get_value_by_date.return_value = 100

        self.wallet_service.sell_stock_and_return_profit(0)

        expect_wallet_amount = before_sell_wallet_amount + 100 * 50 / 100
        self.assertEqual(self.wallet.wallet_amount, expect_wallet_amount)

    def test_sell_stock_and_return_profit_when_profit_more_than_0_should_reduce_wallet_amount_minus_30_percent_of_profit(
            self):
        expect_stock = Stock(
            purchase_date="20-10-2020",
            purchase_value=100,
            share_percentage=50)
        self.wallet.stocks = [
            expect_stock
        ]
        before_sell_wallet_amount = self.wallet.wallet_amount
        self.mock_finance_service.get_value_by_date.return_value = 200

        self.wallet_service.sell_stock_and_return_profit(0)

        expect_wallet_amount = before_sell_wallet_amount + 200 * expect_stock.share_percentage / 100
        profit = 200 * expect_stock.share_percentage / 100 - expect_stock.purchase_value * expect_stock.share_percentage / 100

        self.assertEqual(self.wallet.wallet_amount, expect_wallet_amount - profit * 0.3)

    def test_sell_stock_and_return_profit_should_return_profit(self):
        expect_stock = Stock(
            purchase_date="20-10-2020",
            purchase_value=100,
            share_percentage=50)
        self.wallet.stocks = [
            expect_stock
        ]
        self.mock_finance_service.get_value_by_date.return_value = 200

        result = self.wallet_service.sell_stock_and_return_profit(0)

        expect_profit = (200 - 100) * 50 / 100 * 0.7

        self.assertEqual(result, expect_profit)
