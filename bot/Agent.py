# Dans l'agent, il doit y avoir:
# - qtable
# - best_action
# - discount factor
# - learning rate
# - update avec les rewards
# - les rewards du coup lol
from bot.Action import Action
from bot.State import State
from logic.service.WalletService import WalletService


class Agent:
    def __init__(self, wallet_service: WalletService, learning_rate=1, discount_factor=0.5):
        self.__actions = [Action.BUY, Action.KEEP, Action.SELL]
        self.__wallet_service = wallet_service
        self.__learning_rate = learning_rate
        self.__discount_factor = discount_factor
        self.__qtable = {}
        self.__state = State.LITTLE_LOW
        self.init_qtable()
        self.reset()

    def init_qtable(self):
        for day, row in self.__wallet_service.finance_service.stock_history.iterrows():
            self.__qtable[day] = {}
            for state in self.__wallet_service.finance_service.states:
                self.__qtable[day][state] = {}
                for action in self.__actions:
                    self.__qtable[day][state][action] = 0.0

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
        last_action_profit_percentage = self.__wallet_service.get_last_action_profit_percentage()
        print(f"LAST PROFIT PERC : {last_action_profit_percentage}")
        reward = last_action_profit_percentage ** 2
        return reward if last_action_profit_percentage > 0 else reward * -1

    def update(self, action: Action):
        print(f"NOUVEL ETAT {self.__state}")
        reward = self.calculate_reward()
        print(f"REWARD : {reward}")
        qtable_current_date = self.__qtable[self.__current_date]

        maxQ = max(qtable_current_date[self.__state].values())
        qtable_current_date[self.__state][action] += self.__learning_rate * \
                                                     (reward + self.__discount_factor * maxQ -
                                                      qtable_current_date[self.__state][
                                                          action])
        self.__score += reward

    def can_perform_action(self, action: Action) -> bool:
        match action:
            case Action.BUY:  # TODO Refacto pour les montants
                return self.__wallet_service.can_buy_stock(50)
            case Action.SELL:
                return self.__wallet_service.can_sell_stock()
            case _:
                return True

    def best_action(self):
        best = None
        qtable_current_date = self.__qtable[self.__current_date]
        self.__state = self.__wallet_service.finance_service.get_state_by_date(self.__current_date)

        for action in qtable_current_date[self.__state]:  # par défaut c'est buy...
            print(f"BEST : {best}")
            print(f"Action : {action} Can perform : {self.can_perform_action(action)}")
            if self.can_perform_action(action):
                if not best \
                        or qtable_current_date[self.__state][action] > qtable_current_date[self.__state][best]:
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
            case Action.KEEP:
                self.__wallet_service.keep_stock()
        print(f"ARGENT ACTUEL {self.__wallet_service.get_amount()}")
