import datetime


class Stock:
    def __init__(self, purchase_date: datetime,
                 purchase_value: float):
        self.__purchase_value = purchase_value
        self.__purchase_date = purchase_date

    @property
    def purchase_value(self):
        return self.__purchase_value

    @property
    def purchase_date(self):
        return self.__purchase_date

    def __eq__(self, other):
        if isinstance(other, Stock):
            return self.__purchase_value == other.purchase_value
        return False

    def __str__(self):
        return str(self.__purchase_value) + " " + \
               str(self.__purchase_date)
