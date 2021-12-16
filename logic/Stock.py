class Stock:
    def __init__(self, purchase_date,
                 purchase_value, share_percentage):
        self.__purchase_value = purchase_value
        self.__purchase_date = purchase_date
        self.__share_percentage = share_percentage

    @property
    def purchase_value(self):
        return self.__purchase_value

    @property
    def purchase_date(self):
        return self.__purchase_date

    @property
    def share_percentage(self):
        return self.__share_percentage

    def __eq__(self, other):
        if isinstance(other, Stock):
            return self.__purchase_value == other.purchase_value \
                   and self.__share_percentage == other.share_percentage
        return False

    def __str__(self):
        return str(self.__purchase_value) + " " + \
               str(self.__purchase_date) + " " + \
               str(self.__share_percentage)
