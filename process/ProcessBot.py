import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd

from bot import Agent, Action
from gui import TradingController
from logic import FinanceService, WalletService, Stock


class ProcessBot:
    def __init__(self, finance_service: FinanceService, wallet_service: WalletService,
                 agent: Agent):
        self.__controller: TradingController | None = None
        self.finance_service = finance_service
        self.wallet_service: WalletService = wallet_service
        self.agent: Agent = agent
        self.__last_date = self.finance_service.start_date

        self.__old_wallet_amount = self.wallet_service.get_amount()
        self.__interval = 14
        self.__iteration = 10

    def set_controller(self, controller: TradingController):
        self.__controller = controller
        self.__controller.update_stock_history_info(self.finance_service.stock_name, self.finance_service.start_date,
                                                    self.finance_service.end_date)

    def reset(self):
        self.agent.init_qtable()
        self.agent.reset()

    def process(self):
        d = {'WalletAmount': [], 'Iteration': []}

        if self.__controller is None:
            print("PROBLEM controller not initialize in ProcessBot")
            return

        current_action = Action.BUY
        for i in range(self.__iteration):
            self.agent.reset()
            self.__controller.update_wallet()

            if self.__controller.is_stop is True:
                break

            self.finance_service.define_current_interval(start_date=self.finance_service.start_date + " 00:00:00",
                                                         days=self.__interval)
            self.agent.current_date = str(self.finance_service.current_interval.last_valid_index())

            while self.agent.current_date and self.__controller.is_stop is False:
                rest_days = self.__interval
                while rest_days > 0 and self.__controller.is_stop is False:

                    self.__last_date = self.agent.current_date
                    self.agent.current_date = self.finance_service.next_date(
                        self.agent.current_date)
                    if not self.agent.current_date:
                        break
                    self.__controller.update_current_date(self.agent.current_date)
                    new_action = self.agent.best_action()
                    maybe_stock_bought = self.wallet_service.get_stock(0)
                    current_action = self.__proceed_agent_action_and_update_gui(current_action, new_action,
                                                                                maybe_stock_bought)
                    rest_days = rest_days - 1
                self.finance_service.define_current_interval(
                    str(self.finance_service.current_interval.last_valid_index()), self.__interval)

            self.agent.sell_all_for_the_end(self.__last_date)
            self.__last_date = self.agent.current_date
            self.__controller.empty_stocks_wallet()
            self.__controller.update_wallet()
            d['WalletAmount'].append(self.wallet_service.get_amount())
            d['Iteration'].append(i + 1)
        self.__controller.qtable_controller.reset_qtable()
        self.__controller.qtable_controller.update_qtable(self.agent.qtable)
        self.__controller.stop(())
        self.pretty(self.agent.qtable)

        df = pd.DataFrame(data=d)

        df.plot(y='WalletAmount', x='Iteration')
        plt.title("Apprentissage du bot")
        plt.legend()

        mpf.plot(self.finance_service.stock_history, type="candle", volume=True, figratio=(
            15, 7), style='yahoo', mav=(6, 15), title='spy candle charts')
        plt.show()

    def __proceed_agent_action_and_update_gui(self, current_action: Action, new_action: Action,
                                              maybe_stock_bought: Stock | None):
        if new_action is Action.BUY and maybe_stock_bought is None:
            self.__old_wallet_amount = self.wallet_service.get_amount()

        self.agent.do_action(new_action)
        self.agent.update(new_action, maybe_stock_bought)

        if new_action is Action.SELL:
            benefice = self.wallet_service.get_amount() - self.__old_wallet_amount
            self.__controller.add_new_benefice(benefice=round(benefice, 2), current_date=self.agent.current_date)

        self.__update_stock_in_gui(maybe_stock_bought)
        return self.__update_current_action_in_gui(current_action, new_action)

    def __update_stock_in_gui(self, maybe_stock_bought: Stock | None):
        if maybe_stock_bought is not None:
            self.__controller.update_wallet_and_stock(maybe_stock_bought)

    def __update_current_action_in_gui(self, current_action: Action, new_action: Action):
        if current_action is not new_action:
            self.__controller.update_action(new_action)
            return new_action
        return current_action

    def get_interval(self):
        return self.__interval

    def set_interval(self, new_interval: int):
        self.__interval = new_interval

    @property
    def iteration(self) -> int:
        return self.__iteration

    @iteration.setter
    def iteration(self, iteration: int):
        self.__iteration = iteration

    def pretty(self, d, indent=0):
        for key, value in d.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                self.pretty(value, indent + 1)
            else:
                print('\t' * (indent + 1) + str(value))
