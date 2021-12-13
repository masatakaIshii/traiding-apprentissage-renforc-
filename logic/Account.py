# Récupérer les infos entre deux dates
# Sauvegarder le paquetol
# Faire les calculs au moment de l'achat / vente etc
from logic.IncorrectBuyAmountError import IncorrectBuyAmountError


class Account:
    def __init__(self):
        self.__account_money = 0  # A définir
        self.__actions_money = 0

    def buy(self, action_name, amount):
        if amount > self.account_money:
            raise IncorrectBuyAmountError

        self.__account_money -= amount

    @property
    def account_money(self):
        return self.__account_money

    @property
    def actions_money(self):
        return self.__actions_money

    def set_account_money(self, amount):
        self.__account_money = amount
