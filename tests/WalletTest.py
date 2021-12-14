import unittest

from logic.Wallet import Wallet
from logic.IncorrectBuyAmountError import IncorrectBuyAmountError


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.Wallet = Wallet()

    def test_buy_should_retire_money_from_wallet(self):
        self.Wallet.set_wallet_amount(100)
        self.Wallet.buy("AAPL", 50)
        self.assertEqual(50, self.Wallet.wallet_amount)

    def test_buy_amount_should_be_inferior_to_money(self):
        self.Wallet.set_wallet_amount(100)
        with self.assertRaises(IncorrectBuyAmountError):
            self.Wallet.buy("AAPL", 120)

    # ajouter le mock du service
    # d u coup faudra créer un service
    def test_buy_should_add_stock_in_wallet_stocks(self):
        self.Wallet.set_wallet_amount(1000)
        self.Wallet.buy("AAPL", 100)
        self.assertEqual()


if __name__ == '__main__':
    unittest.main()
