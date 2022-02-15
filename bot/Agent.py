from bot.Action import Action
from logic.Stock import Stock
from logic.service.WalletService import WalletService

REWARD_FORBIDDEN_ACTION = -10000


class Agent:
    def __init__(self, wallet_service: WalletService, learning_rate=0.5, discount_factor=1):
        self.__actions = [Action.BUY, Action.KEEP, Action.SELL]
        self.__wallet_service = wallet_service
        self.__learning_rate = learning_rate
        self.__discount_factor: float = discount_factor
        self.__able_to_buy = True
        self.__qtable = {}
        self.__did_forbidden_action = False
        self.init_qtable()
        self.reset()

    def init_qtable(self):
        self.__qtable = {}
        for state in range(self.__wallet_service.finance_service.category_number):
            self.__qtable[state] = {}
            for stock_state in [False, True]:
                self.__qtable[state][stock_state] = {}
                if not stock_state:
                    for able_to_buy in [False, True]:
                        self.__qtable[state][stock_state][able_to_buy] = {}
                        for action in self.__actions:
                            self.__qtable[state][stock_state][able_to_buy][action] = 0.0
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

    @property
    def learning_rate(self) -> float:
        return self.__learning_rate

    @learning_rate.setter
    def learning_rate(self, learning_rate: float):
        self.__learning_rate = learning_rate

    @property
    def discount_factor(self) -> float:
        return self.__discount_factor

    @discount_factor.setter
    def discount_factor(self, discount_factor: float):
        self.__discount_factor = discount_factor

    def get_current_money_amount(self):
        return self.__wallet_service.get_amount()

    def reset(self):
        self.__wallet_service.reset()
        self.__score = 0

    def calculate_reward_sell(self, stock: Stock | None) -> float:
        return self.__wallet_service.finance_service \
            .get_variation_percentage(self.__wallet_service.finance_service.get_value_by_date(self.__current_date),
                                      stock.purchase_value)

    def calculate_reward_keep(self, stock: Stock | None) -> float:

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

        reward = last_action_profit_percentage ** 2
        return reward if last_action_profit_percentage > 0 else reward * -1

    def update(self, action: Action, maybe_stock_bought: Stock | None):

        reward = self.calculate_reward(action, stock=maybe_stock_bought)

        if maybe_stock_bought is None:
            able_to_buy = self.__able_to_buy
            maxQ = max(self.__qtable[self.__state][False][able_to_buy].values())
            self.__qtable[self.__state][False][able_to_buy][action] += round(self.__learning_rate * \
                                                                             (reward + self.__discount_factor * maxQ -
                                                                              self.__qtable[self.__state][False][
                                                                                  able_to_buy][
                                                                                  action]), 2)
        else:
            bought_stock_state = self.__wallet_service.finance_service.get_state_by_date(
                maybe_stock_bought.purchase_date)

            maxQ = max(self.__qtable[self.__state][True][bought_stock_state].values())

            self.__qtable[self.__state][True][bought_stock_state][action] += round(self.__learning_rate * \
                                                                                   (
                                                                                           reward + self.__discount_factor * maxQ -
                                                                                           self.__qtable[
                                                                                               self.__state][True][
                                                                                               bought_stock_state][
                                                                                               action]), 2)
        self.__score += reward

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
            able_to_buy = self.is_able_to_buy()
            for action in qtable[False][able_to_buy]:
                if not best \
                        or qtable[False][able_to_buy][action] > qtable[False][able_to_buy][best]:
                    best = action
        return best

    def sell_all_for_the_end(self, date: str):
        if self.__wallet_service.contains_stock():
            self.__wallet_service.sell_stock_and_return_profit(0, date)

    def is_able_to_buy(self) -> bool:
        return True if self.__wallet_service.get_amount() - self.__wallet_service.finance_service.get_value_by_date(
            self.__current_date) >= 0 else False

    def do_action(self, action: Action):

        self.__did_forbidden_action = False
        self.__able_to_buy = self.is_able_to_buy()
        match action:
            case Action.BUY:
                if self.__wallet_service.contains_stock():
                    self.__did_forbidden_action = True
                else:
                    try:
                        self.__wallet_service.buy_stock(self.__current_date)
                    except:
                        self.__did_forbidden_action = True

            case Action.SELL:
                if self.__wallet_service.contains_stock():
                    self.__wallet_service.sell_stock_and_return_profit(0, self.__current_date)
                else:
                    self.__did_forbidden_action = True
