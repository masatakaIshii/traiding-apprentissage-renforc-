import unittest

from logic.Account import Account
from logic.IncorrectBuyAmountError import IncorrectBuyAmountError


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.Account = Account()

    def test_buy_should_retire_money_from_account(self):
        self.Account.set_account_money(100)
        self.Account.buy("AAPL", 50)
        self.assertEqual(50, self.Account.account_money)

    def test_buy_amount_should_be_inferior_to_money(self):
        self.Account.set_account_money(100)
        with self.assertRaises(IncorrectBuyAmountError):
            self.Account.buy("AAPL", 120)


if __name__ == '__main__':
    unittest.main()
