# Dans l'agent, il doit y avoir:
# - qtable
# - best_action
# - discount factor
# - learning rate
# - update avec les rewards
# - les rewards du coup lol
from bot.Action import Action
from logic.service.WalletService import WalletService


class Agent:
    def __init__(self, wallet_service: WalletService, learning_rate=1, discount_factor=0.5):
        self.__actions = [Action.BUY, Action.KEEP, Action.SELL]
        self.__wallet_service = wallet_service
        self.__learning_rate = learning_rate
        self.__discount_factor = discount_factor
        self.__qtable = {}
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

    def get_current_money_amount(self):
        return self.__wallet_service.get_amount()

    # Remet tout à zéro lol
    def reset(self):
        self.__wallet_service.reset()
        self.__score = 0

    def calculate_reward(self) -> float:
        last_action_profit_percentage = self.__wallet_service.get_last_action_profit_percentage(self.__current_date)
        print(f"LAST PROFIT PERC : {last_action_profit_percentage}")
        # if last_action_profit_percentage == 0:
        #     last_action_profit_percentage = -10
        reward = last_action_profit_percentage ** 2
        return reward if last_action_profit_percentage > 0 else reward * -1

    def update(self, action: Action):
        print(f"NOUVEL ETAT {self.__state}")
        reward = self.calculate_reward()
        print(f"REWARD : {reward}")
        # TODO faut d'abord voir si on a bought du coup
        has_bought = self.__wallet_service.has_bought()
        if not has_bought:
            maxQ = max(self.__qtable[self.__state][False].values())
            self.__qtable[self.__state][False][action] += self.__learning_rate * \
                                                          (reward + self.__discount_factor * maxQ -
                                                           self.__qtable[self.__state][False][
                                                               action])
        else:
            bought_stock_state = self.__wallet_service.finance_service.get_state_by_date(
                self.__wallet_service.get_stock(0).purchase_date)
            maxQ = max(self.__qtable[self.__state][True][bought_stock_state].values())

            self.__qtable[self.__state][True][bought_stock_state][action] += self.__learning_rate * \
                                                                             (reward + self.__discount_factor * maxQ -
                                                                              self.__qtable[self.__state][True][
                                                                                  bought_stock_state][
                                                                                  action])
        self.__score += reward
        self.__wallet_service.update_last_amount(self.__current_date)
        # TODO Update le last amount ici

    def can_perform_action(self, action: Action) -> bool:
        match action:
            case Action.BUY:  # TODO Refacto pour les montants
                return self.__wallet_service.can_buy_stock(50)
            case Action.SELL:
                return self.__wallet_service.has_bought()
            case _:
                return True

    def best_action(self):
        best = None
        self.__state = self.__wallet_service.finance_service.get_state_by_date(self.__current_date)
        qtable = self.__qtable[self.__state]

        if self.__wallet_service.has_bought():
            bought_stock_state = self.__wallet_service.finance_service.get_state_by_date(
                self.__wallet_service.get_stock(0).purchase_date)
            for action in qtable[True][bought_stock_state]:
                if self.can_perform_action(action):
                    if not best \
                            or qtable[True][bought_stock_state][action] > qtable[True][bought_stock_state][best]:
                        best = action
        else:

            for action in qtable[False]:
                if self.can_perform_action(action):
                    if not best \
                            or qtable[False][action] > qtable[False][best]:
                        best = action
        return best

    def do_action(self, action: Action):
        match action:
            case Action.BUY:
                # TODO je ne sais pas quoi mettre pour le montant
                self.__wallet_service.buy_stock(self.__current_date, 50)
            case Action.SELL:
                # TODO je ne vois pas comment faire avec plusieurs stocks pour l'instant
                self.__wallet_service.sell_stock_and_return_profit(0, self.__current_date)
            # case Action.KEEP:
            #     self.__wallet_service.keep_stock()
        print(f"ARGENT ACTUEL {self.__wallet_service.get_amount()}")
