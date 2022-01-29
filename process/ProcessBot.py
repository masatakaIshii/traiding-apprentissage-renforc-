from bot import Agent
from gui import TradingController
from logic import FinanceService, WalletService


class ProcessBot:
    def __init__(self, finance_service: FinanceService, wallet_service: WalletService,
                 agent: Agent):
        self.__controller = None
        self.finance_service = finance_service
        self.wallet_service: WalletService = wallet_service
        self.agent: Agent = agent

    def set_controller(self, controller: TradingController):
        self.__controller = controller

    def process(self, start_date: str = "2018-12-31", days: int = 14):
        if self.__controller is None:
            print("PROBLEM controller not initialize in ProcessBot")
            return

        for i in range(5):
            self.finance_service.define_current_interval(start_date=start_date, days=days)
            self.agent.current_date = str(self.finance_service.current_interval.last_valid_index())

            while self.agent.current_date:
                rest_days = days
                while rest_days > 0:
                    self.agent.current_date = self.finance_service.next_date(
                        self.agent.current_date)  # on est sur la date d'après
                    # print(f"current date : {self.agent.current_date}")
                    if not self.agent.current_date:
                        break
                    # print(f"CURRENT DATE : {self.agent.current_date}")
                    action = self.agent.best_action()
                    # print(f"BEST ACTION : {action}")
                    maybe_stock_bought = self.wallet_service.get_stock(0)
                    # if action is Action.BUY:
                    #     maybe_stock_bought = None
                    self.agent.do_action(action)
                    self.agent.update(action, maybe_stock_bought)

                    rest_days = rest_days - 1
                self.finance_service.define_current_interval(
                    str(self.finance_service.current_interval.last_valid_index()), days)

        self.pretty(self.agent.qtable)

    def pretty(self, d, indent=0):
        for key, value in d.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                self.pretty(value, indent + 1)
            else:
                print('\t' * (indent + 1) + str(value))
