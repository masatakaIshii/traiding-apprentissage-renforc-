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
        self.__str_wallet_actions: List[string] = []
        self.__view.start_button.bind("<Button>", self.start)
        self.__view.set_wallet_amount(self.__wallet_service.get_amount())
        self.__view.set_current_date(self.__current_date)

        self.__old_wallet_amount = self.__wallet_service.get_amount()

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
        agent = Agent(self.__wallet_service)
        max_value = -10000
        iteration = 1
        temp_action = Action.BUY
        while iteration < 1000 and self.__is_pause is False:
            count = 1
            agent.reset()
            self.__view.set_count_bot_iter(count=iteration)
            temp_action = self.__one_iter(agent, count, temp_action)

            if agent.score > max_value:
                max_value = agent.score
                iteration = iteration + 1
        print(f"MAX SCORE : {max_value} à la boucle {iteration}")

    def __one_iter(self, agent: Agent, curren_count: int, current_action: Action | None) -> Action:
        finance_service = self.__wallet_service.finance_service
        count = curren_count

        iter_wesh = 0
        for date, stock in finance_service.stock_history.iterrows():
            if self.__is_pause is True:
                break
            time.sleep(0.1)
            agent.current_date = date
            self.__view.set_current_date(date)
            new_action = agent.best_action()
            self.agent_action_and_update(agent, new_action)

            if current_action is not new_action:
                self.__view.update_action_labels_depend_to_action(new_action)
                current_action = new_action
            self.__update_wallet_and_stock(stock=stock)
            count += 1

            if new_action is Action.SELL and iter_wesh == 3:
                self.pause()
            elif new_action is Action.SELL:
                iter_wesh = iter_wesh + 1
        print(f"Count ======================> {count}")
        return current_action

    def agent_action_and_update(self, agent: Agent, action: Action):
        if action is Action.BUY and self.__wallet_service.get_stock(0) is None:
            self.__old_wallet_amount = self.__wallet_service.get_amount()

        agent.do_action(action)
        agent.update(action)

        if action is Action.SELL:
            benefice = self.__wallet_service.get_amount() - self.__old_wallet_amount
            self.__view.insert_benefice_in_list(benefice=round(benefice, 2), date=agent.current_date)

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
        return self.__str_wallet_actions
