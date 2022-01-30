import unittest

from logic.FinanceService import FinanceService


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.FinanceService = FinanceService()


if __name__ == '__main__':
    unittest.main()
