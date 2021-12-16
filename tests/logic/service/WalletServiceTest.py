import unittest
from datetime import date
from unittest.mock import MagicMock, PropertyMock

from logic.Stock import Stock
from logic.Wallet import Wallet
from logic.exceptions.IncorrectBuyAmountError import IncorrectBuyAmountError
from logic.service.WalletService import WalletService


class WalletServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_finance_service = MagicMock()
        self.mock_wallet = Wallet()
        self.wallet_service = WalletService(self.mock_wallet, self.mock_finance_service)

    # get_amount
    def test_get_amount_should_return_amount_of_wallet(self):
        wallet_amount = 33
        mock_wallet_amount = PropertyMock(return_value=wallet_amount)
        type(self.mock_wallet).wallet_amount = mock_wallet_amount

        self.assertEqual(wallet_amount, self.wallet_service.get_amount())

    # buy_stock
    def test_buy_stock_should_reduce_amount_of_wallet_depend_to_found_stock(self):
        today_str = date.today().strftime('%m-%d-%Y')
        purchase_value = 36
        share_percentage = 50
        self.mock_finance_service.get_stock.return_value = Stock(today_str, purchase_value, share_percentage)
        wallet_amount = self.mock_wallet.wallet_amount
        self.assertEqual(100, wallet_amount)
        self.wallet_service.buy_stock(today_str, share_percentage)

        self.assertEqual(100 - 36 * 0.5, self.wallet_service.get_amount())

    def test_buy_stock_after_bought_stock_should_add_in_wallet(self):
        today = date.today().strftime('%m-%d-%Y')
        purchase_value = 36
        share_percentage = 50
        self.mock_finance_service.get_stock.return_value = Stock(today, purchase_value, share_percentage)

        len_stock = len(self.mock_wallet.stocks)

        self.wallet_service.buy_stock(today, share_percentage)

        self.assertEqual(len_stock + 1, len(self.mock_wallet.stocks))

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

    # get_stocks
    def test_get_stocks_should_return_all_stocks_on_wallet(self):
        stocks = [
            Stock("20-10-2020", 5, 4)
        ]
        type(self.mock_wallet).stocks = PropertyMock(return_value=stocks)

        result = self.wallet_service.get_stocks()

        self.assertEqual(result, stocks)

    # get_stock
    def test_get_stock_should_get_stocks_of_wallet(self):
        stocks = [
            Stock("20-10-2020", 5, 4)
        ]
        mock_stocks = PropertyMock(return_value=stocks)
        type(self.mock_wallet).stocks = mock_stocks

        self.wallet_service.get_stock(0)
        mock_stocks.assert_called_once()

    def test_get_stock_should_get_one_stock_based_on_stocks_by_index(self):
        expect_stock = Stock("20-10-2020", 5, 4)
        stocks = [
            expect_stock
        ]
        mock_stocks = PropertyMock(return_value=stocks)
        type(self.mock_wallet).stocks = mock_stocks

        result = self.wallet_service.get_stock(0)

        self.assertEqual(result, expect_stock)

    def test_get_stock_should_return_none_when_index_equal_than_len_of_stocks(self):
        expect_stock = Stock("20-10-2020", 5, 4)
        stocks = [
            expect_stock
        ]
        mock_stocks = PropertyMock(return_value=stocks)
        type(self.mock_wallet).stocks = mock_stocks

        cur_index = 1

        result = self.wallet_service.get_stock(cur_index)

        self.assertEqual(len(stocks), cur_index)
        self.assertIsNone(result)

    def test_sell_stock_should_get_stocks_of_wallet(self):
        expect_stock = Stock("20-10-2020", 5, 4)
        stocks = [
            expect_stock
        ]
        mock_stocks = PropertyMock(return_value=stocks)
        type(self.mock_wallet).stocks = mock_stocks

        self.wallet_service.sell_stock(0)

        mock_stocks.assert_called()

    def test_sell_stock_oscours_jenecomprendpascequejefais(self):
        self.assertNotEqual("En espérant demain ça va se résoudre",
                            "désolé pour ce test, bon j'ai vu aussi pire l'année dernière mais je ne dénonce pas")
