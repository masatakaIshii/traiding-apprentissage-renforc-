import string
import threading
import time
from tkinter import Tk
from typing import List

from bot.Action import Action
from bot.Agent import Agent
from gui.TradingView import TradingView
from logic.service.WalletService import WalletService


class TradingController:
    def __init__(self, master: Tk, wallet_service: WalletService, view: TradingView):
        self.__master = master
        self.__wallet_service = wallet_service
        self.__view = view

        self.__current_date = self.__wallet_service.finance_service.get_first_date_of_stock_history()
        self.__str_actions: List[string] = []
        self.__view.start_button.bind("<Button>", self.start)
        self.__view.set_wallet_amount(self.__wallet_service.get_amount())
        self.__view.set_current_date(self.__current_date)

        self.__set_master_tk()
        self.__is_pause = True

    def __set_master_tk(self):
        self.__master.minsize(780, 780)
        self.__master.title("Trading bot")

        self.__master.mainloop()

    def start(self, _):
        self.__view.start_button_clicked()
        self.__view.start_button.unbind("<Button>")
        self.__view.pause_button.bind("<Button>", self.pause)
        print("controller start")
        self.__is_pause = False

        threading.Thread(target=self.process).start()

    def process(self):
        finance_service = self.__wallet_service.finance_service
        agent = Agent(self.__wallet_service)
        max_value = -10000
        iteration = 1
        temp_action = Action.BUY
        while iteration < 1000 and self.__is_pause is False:
            count = 1
            agent.reset()
            self.__view.set_count_bot_iter(count=iteration)
            for date, stock in finance_service.stock_history.iterrows():
                if self.__is_pause is True:
                    break
                time.sleep(0.1)
                agent.current_date = date
                self.__view.set_current_date(date)
                action = agent.best_action()
                agent.do_action(action)
                agent.update(action)
                if temp_action is not action:
                    self.__view.update_action_labels_depend_to_action(action)
                    temp_action = action
                self.__update_wallet_and_stock(stock=stock)

                count += 1

            if agent.score > max_value:
                max_value = agent.score
                iteration = iteration + 1
        print(f"MAX SCORE : {max_value} à la boucle {iteration}")

    def pause(self, _):
        self.__view.pause_button_clicked()
        self.__view.pause_button.unbind("<Button>")
        self.__view.start_button.bind("<Button>", self.start)
        print("controller pause")
        self.__is_pause = True

    def __update_wallet_and_stock(self, stock):
        your_stock = self.__wallet_service.get_stock(0)
        if your_stock is not None:
            self.__view.set_your_stock_amount(round(your_stock.purchase_value * your_stock.share_percentage / 100, 2))
        else:
            self.__view.set_your_stock_amount(None)
        wallet_amount = round(self.__wallet_service.get_amount(), 2)
        self.__view.set_wallet_amount(wallet_amount)
        self.__view.set_cur_stock_amount(round(stock['Open'], 2))

    @property
    def str_actions(self):
        return self.__str_actions
