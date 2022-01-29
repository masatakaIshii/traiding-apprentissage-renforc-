import string
import threading
from tkinter import Tk
from typing import List

from bot.Action import Action
from bot.Agent import Agent
from gui import TradingView, QTableController
from logic import Stock
from process import ProcessBot


class TradingController:
    def __init__(self, view: TradingView, qtable_controller: QTableController,process_bot: ProcessBot):
        self.__process_bot = process_bot
        self.__wallet_service = process_bot.wallet_service
        self.__view = view
        self.__agent: Agent = process_bot.agent
        self.qtable_controller = qtable_controller

        self.__current_date = self.__wallet_service.finance_service.get_first_date_of_stock_history()
        self.__str_wallet_actions: List[string] = []
        self.__view.start_button.bind("<Button>", self.start)
        self.__view.set_wallet_amount(self.__wallet_service.get_amount())
        self.__view.set_current_date(self.__current_date)

        self.__old_wallet_amount = self.__wallet_service.get_amount()

        self.__process_bot.set_controller(self)
        self.__is_stop = True

    def start(self, _):
        self.__view.start_button_clicked()
        self.__view.start_button.unbind("<Button>")
        self.__view.stop_button.bind("<Button>", self.stop)
        print("controller start")
        self.__is_stop = False

        self.__process_bot.reset()
        self.update_wallet()
        threading.Thread(target=self.__process_bot.process).start()

    def update_current_date(self, new_date: str):
        self.__view.set_current_date(new_date)

    def update_action(self, action: Action):
        self.__view.update_action_labels_depend_to_action(action=action)

    def add_new_benefice(self, benefice: float, current_date: str):
        self.__view.insert_benefice_in_list(benefice=benefice, date=current_date)

    def stop(self, _):
        self.__view.stop_button_clicked()
        self.__view.stop_button.unbind("<Button>")
        self.__view.start_button.bind("<Button>", self.start)
        print("controller stop")
        self.__is_stop = True

    def update_wallet(self):
        wallet_amount = round(self.__wallet_service.get_amount(), 2)
        self.__view.set_wallet_amount(wallet_amount)

    def update_wallet_and_stock(self, stock: Stock):
        your_stock = self.__wallet_service.get_stock(0)
        if your_stock is not None:
            self.__view.set_your_stock_amount(round(your_stock.purchase_value * your_stock.share_percentage / 100, 2))
        else:
            self.__view.set_your_stock_amount(None)
        self.update_wallet()
        # TODO : pas sûr
        self.__view.set_cur_stock_amount(round(stock.purchase_value, 2))

    @property
    def str_actions(self):
        return self.__str_wallet_actions

    @property
    def is_stop(self):
        return self.__is_stop
