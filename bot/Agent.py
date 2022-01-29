# Dans l'agent, il doit y avoir:
# - qtable
# - best_action
# - discount factor
# - learning rate
# - update avec les rewards
# - les rewards du coup lol
from bot.Action import Action
from logic.Stock import Stock
from logic.service.WalletService import WalletService

REWARD_FORBIDDEN_ACTION = -10000


class Agent:
    def __init__(self, wallet_service: WalletService, learning_rate=0.5, discount_factor=1):
        self.__actions = [Action.BUY, Action.KEEP, Action.SELL]
        self.__wallet_service = wallet_service
        self.__learning_rate = learning_rate
        self.__discount_factor = discount_factor
        self.__qtable = {}
        self.__did_forbidden_action = False
        self.init_qtable()
        self.reset()

    def init_qtable(self):
        for state in range(self.__wallet_service.finance_service.category_number):
            self.__qtable[state] = {}
            for stock_state in [False, True]:
                self.__qtable[state][stock_state] = {}
                if not stock_state:
                    for action in self.__actions:
                        self.__qtable[state][stock_state][action] = 0.0
                else:
                    for bought_stock_state in range(self.__wallet_service.finance_service.category_number):
                        self.__qtable[state][stock_state][bought_stock_state] = {}
                        for action in self.__actions:
                            self.__qtable[state][stock_state][bought_stock_state][action] = 0.0

    @property
    def current_date(self):
        return self.__current_date

    @current_date.setter
    def current_date(self, date: str):
        self.__current_date = date

    @property
    def state(self):
        return self.__state

    @property
    def score(self):
        return self.__score

    @property
    def qtable(self):
        return self.__qtable

    @property
    def wallet_service(self) -> WalletService:
        return self.__wallet_service

    # @property
    # def wallet_service(self) -> WalletService:
    #     return self.__wallet_service
    #
    # @wallet_service.setter
    # def wallet_service(self, value: WalletService):
    #     self.__wallet_service = value

    def get_current_money_amount(self):
        return self.__wallet_service.get_amount()

    # Remet tout à zéro lol
    def reset(self):
        self.__wallet_service.reset()
        self.__score = 0

    def calculate_reward_sell(self, stock: Stock | None) -> float:
        return self.__wallet_service.finance_service \
            .get_variation_percentage(self.__wallet_service.finance_service.get_value_by_date(self.__current_date),
                                      stock.purchase_value / (stock.share_percentage / 100))

    def calculate_reward_keep(self, stock: Stock | None) -> float:
        print(f"STOCK : {stock}")
        if stock is None:
            return self.__wallet_service.get_variation_with_average(self.__current_date)

        return self.__wallet_service.finance_service.get_variation_percentage(
            self.__wallet_service.get_amount() + stock.purchase_value
            , self.__wallet_service.get_potential_amount(self.__current_date))

    def calculate_reward_buy(self) -> float:
        return self.__wallet_service.get_variation_with_average(self.__current_date) * -1

    def calculate_reward(self, action: Action, stock: Stock | None) -> float:
        if self.__did_forbidden_action:
            return REWARD_FORBIDDEN_ACTION
        if action is Action.SELL:
            last_action_profit_percentage = self.calculate_reward_sell(stock)
        elif action is Action.KEEP:
            last_action_profit_percentage = self.calculate_reward_keep(stock)
        elif action is Action.BUY:
            last_action_profit_percentage = self.calculate_reward_buy()
        else:
            last_action_profit_percentage = 0

        print(f"LAST PROFIT PERC : {last_action_profit_percentage}")
        reward = last_action_profit_percentage ** 2
        return reward if last_action_profit_percentage > 0 else reward * -1

    def update(self, action: Action, maybe_stock_bought: Stock | None):
        # print(f"ETAT ACTUEL {self.__state}")
        reward = self.calculate_reward(action, stock=maybe_stock_bought)
        print(f"REWARD : {reward}")

        if maybe_stock_bought is None:
            maxQ = max(self.__qtable[self.__state][False].values())
            self.__qtable[self.__state][False][action] += round(self.__learning_rate * \
                                                                (reward + self.__discount_factor * maxQ -
                                                                 self.__qtable[self.__state][False][
                                                                     action]), 2)
        else:
            bought_stock_state = self.__wallet_service.finance_service.get_state_by_date(
                maybe_stock_bought.purchase_date)
            # print(f"STOCK STATE : {bought_stock_state}")
            maxQ = max(self.__qtable[self.__state][True][bought_stock_state].values())

            self.__qtable[self.__state][True][bought_stock_state][action] += round(self.__learning_rate * \
                                                                                   (
                                                                                           reward + self.__discount_factor * maxQ -
                                                                                           self.__qtable[
                                                                                               self.__state][True][
                                                                                               bought_stock_state][
                                                                                               action]), 2)
        self.__score += reward
        self.__wallet_service.update_last_amount(self.__current_date)
        # TODO Update le last amount ici

    # def can_perform_action(self, action: Action) -> bool:
    #     match action:
    #         case Action.BUY:  # TODO Refacto pour les montants
    #             return self.__wallet_service.can_buy_stock(50)
    #         case Action.SELL:
    #             return self.__wallet_service.contains_stock()
    #         case _:
    #             return True

    def best_action(self):
        best = None
        self.__state = self.__wallet_service.finance_service.get_state_by_date(self.__current_date)
        qtable = self.__qtable[self.__state]

        if self.__wallet_service.contains_stock():
            bought_stock_state = self.__wallet_service.finance_service.get_state_by_date(
                self.__wallet_service.get_stock(0).purchase_date)
            for action in qtable[True][bought_stock_state]:
                if not best \
                        or qtable[True][bought_stock_state][action] > qtable[True][bought_stock_state][best]:
                    best = action
        else:

            for action in qtable[False]:
                if not best \
                        or qtable[False][action] > qtable[False][best]:
                    best = action
        return best

    def do_action(self, action: Action):
        print(f"ACTION : {action}")
        print(f"SELF CATEGORIE : {self.__state}")
        self.__did_forbidden_action = False
        match action:
            case Action.BUY:
                if self.__wallet_service.contains_stock():
                    self.__did_forbidden_action = True
                else:
                    try:
                        self.__wallet_service.buy_stock(self.__current_date, 50)
                    except:
                        self.__did_forbidden_action = True

            case Action.SELL:
                if self.__wallet_service.contains_stock():
                    self.__wallet_service.sell_stock_and_return_profit(0, self.__current_date)
                else:
                    self.__did_forbidden_action = True

            # case Action.KEEP:
            #     self.__wallet_service.keep_stock()
        print(f"ARGENT ACTUEL {self.__wallet_service.get_amount()}")
