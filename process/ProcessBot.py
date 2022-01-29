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

        self.__old_wallet_amount = self.wallet_service.get_amount()

    def set_controller(self, controller: TradingController):
        self.__controller = controller

    def reset(self):
        self.agent.init_qtable()
        self.agent.reset()

    def process(self, start_date: str = "2018-12-31", days: int = 14):
        if self.__controller is None:
            print("PROBLEM controller not initialize in ProcessBot")
            return

        current_action = Action.BUY
        for i in range(5):
            if self.__controller.is_stop is True:
                break
            self.finance_service.define_current_interval(start_date=start_date, days=days)
            self.agent.current_date = str(self.finance_service.current_interval.last_valid_index())

            while self.agent.current_date and self.__controller.is_stop is False:
                rest_days = days
                while rest_days > 0 and self.__controller.is_stop is False:
                    # time.sleep(0.2)
                    self.agent.current_date = self.finance_service.next_date(
                        self.agent.current_date)  # on est sur la date d'après
                    if not self.agent.current_date:
                        break
                    self.__controller.update_current_date(self.agent.current_date)
                    new_action = self.agent.best_action()
                    maybe_stock_bought = self.wallet_service.get_stock(0)
                    current_action = self.__proceed_agent_action_and_update_gui(current_action, new_action,
                                                                                maybe_stock_bought)
                    rest_days = rest_days - 1
                self.finance_service.define_current_interval(
                    str(self.finance_service.current_interval.last_valid_index()), days)

        self.__controller.qtable_controller.reset_qtable()
        self.__controller.qtable_controller.update_qtable(self.agent.qtable)
        self.__controller.stop(())

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

    def pretty(self, d, indent=0):
        for key, value in d.items():
            print('\t' * indent + str(key))
            if isinstance(value, dict):
                self.pretty(value, indent + 1)
            else:
                print('\t' * (indent + 1) + str(value))
