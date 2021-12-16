import unittest

from logic.FinanceService import FinanceService
from logic.Stock import Stock
from logic.exceptions.StockNotFoundError import StockNotFoundError


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.FinanceService = FinanceService()

    # def test_get_stock_should_return_exception_wrong_name(self):
    #     with self.assertRaises(StockNotFoundError):
    #         self.FinanceService.get_stock("", "", 2000)
    #
    # def test_get_stock_should_return_stock_by_name(self):
    #     stock = Stock("AAPL", "1999-03-03", 200, 0.4)
    #     self.assertEqual(stock, self.FinanceService.get_stock("AAPL", "1999-03-03", 200))
    #

if __name__ == '__main__':
    unittest.main()
