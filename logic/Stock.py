class Stock:
    def __init__(self, name, purchase_date,
                 purchase_value, share_percentage):
        self.__name = name
        self.__purchase_value = purchase_value
        self.__purchase_date = purchase_date
        self.__share_percentage = share_percentage

    @property
    def name(self):
        return self.__name

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
            return self.__name == other.name \
                   and self.__purchase_value == other.purchase_value \
                   and self.__share_percentage == other.share_percentage
        return False
