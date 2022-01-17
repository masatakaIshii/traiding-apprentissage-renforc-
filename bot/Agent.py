# Dans l'agent, il doit y avoir:
# - qtable
# - best_action
# - discount factor
# - learning rate
# - update avec les rewards
# - les rewards du coup lol
from bot.Action import Action
from bot.Reward import Reward
from bot.State import State
from logic.service.WalletService import WalletService

REWARD_VERY_HIGH = 1000
REWARD_HIGH = 500
REWARD_LITTLE_HIGH = 200
REWARD_LITTLE_LOW = -200
REWARD_LOW = -500
REWARD_VERY_LOW = -1000


class Agent:
    def __init__(self, wallet_service: WalletService, learning_rate=1, discount_factor=0.5):
        self.__states = [State.VERY_LOW, State.LOW, State.LITTLE_LOW, State.LITTLE_HIGH, State.HIGH, State.VERY_HIGH]
        self.__actions = [Action.BUY, Action.KEEP, Action.SELL]
        self.__wallet_service = wallet_service
        self.__learning_rate = learning_rate
        self.__discount_factor = discount_factor
        self.__qtable = {}
        self.init_qtable()
        self.reset()

    def init_qtable(self):
        for day, row in self.__wallet_service.finance_service.stock_history.iterrows():
            self.__qtable[day] = {}
            for state in self.__states:
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

    def reset(self):
        self.__state = State.LITTLE_HIGH
        self.__score = 0

    # Est-ce que notre state est définit à chaqeu fois ou seulement quand on vend ?
    # Nan il faut update le state à chaque fois, donc faut savoir en permanence combien on perd / gagne virtuellement
    def define_state(self) -> State:
        profit_percentage = self.__wallet_service.get_profit_percentage()
        print(f"PROFIT POURCENTAGE : {profit_percentage}")
        if 0 > profit_percentage > -10:
            return State.LITTLE_LOW
        elif -10 > profit_percentage > -30:
            return State.LOW
        elif profit_percentage < -30:
            return State.VERY_LOW
        elif 0 < profit_percentage < 10:
            return State.LITTLE_HIGH
        elif 10 < profit_percentage < 30:
            return State.HIGH
        else:
            return State.VERY_HIGH

    # TODO A DEBATTRE POUR LE CACLUL DE LA REWARD
    # Prendre le pourcentage d'argent gagné sur la dernière action
    # Donc il nous faut tout le temps l'argent actuel et celui de juste avant
    def calculate_reward(self, state: State) -> float:
        match state:
            case State.VERY_LOW:
                return Reward.VERY_LOW.value
            case State.LOW:
                return Reward.LOW.value
            case State.LITTLE_LOW:
                return Reward.LITTLE_LOW.value
            case State.LITTLE_HIGH:
                return Reward.LITTLE_HIGH.value
            case State.HIGH:
                return Reward.HIGH.value
            case State.VERY_HIGH:
                return Reward.VERY_HIGH.value
            case _:
                return 0

    # Avec catégorie précédente
    # def calculate_reward(self, old_state: State, new_state: State) -> float:
    #     state_value = new_state.value - old_state.value
    #     reward = state_value ** 2 * 100
    #     return reward if state_value > 0 else reward * -1

    # Avec argent précédent
    # def calculate_reward(self) -> float:
    #     last_action_profit_percentage = self.__wallet_service.get_last_action_profit_percentage()
    #     print(f"LAST PROFIT PERC : {last_action_profit_percentage}")
    #     reward = last_action_profit_percentage ** 2
    #     return reward if last_action_profit_percentage > 0 else reward * -1

    def update(self, action: Action):
        new_state = self.define_state()
        print(f"NOUVEL ETAT {new_state}")
        reward = self.calculate_reward(new_state)
        print(f"REWARD : {reward}")
        qtable_current_date = self.__qtable[self.__current_date]

        maxQ = max(qtable_current_date[new_state].values())
        qtable_current_date[self.__state][action] += self.__learning_rate * \
                                                     (reward + self.__discount_factor * maxQ -
                                                      qtable_current_date[self.__state][
                                                          action])
        self.__state = new_state
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
