# Dans l'agent, il doit y avoir:
# - qtable
# - best_action
# - discount factor
# - learning rate
# - update avec les rewards
# - les rewards du coup lol
from bot.Action import Action
from bot.State import State

REWARD_VERY_HIGH = 1000
REWARD_HIGH = 500
REWARD_LITTLE_HIGH = 200
REWARD_LITTLE_LOW = -200
REWARD_LOW = -500
REWARD_VERY_LOW = -1000

class Agent:
    def __init__(self, environment, learning_rate=1, discount_factor=0.5):
        self.__states = [State.VERY_LOW, State.LOW, State.LITTLE_LOW, State.LITTLE_HIGH, State.HIGH, State.VERY_HIGH]
        self.__actions = [Action.BUY, Action.KEEP, Action.SELL]
        self.__learning_rate = learning_rate
        self.__discount_factor = discount_factor
        self.__environment = environment
        self.__qtable = {}

        for s in self.__states:
            self.__qtable[s] = {}
            for a in self.__actions:
                self.__qtable[s][a] = 0.0
        self.reset()

    def reset(self):
        self.__state = State.LITTLE_LOW
        self.__score = 0

    def update(self, state, action, reward):
        maxQ = max(self.__qtable[state].values())
        self.__qtable[self.__state][action] += self.__learning_rate * \
                                               (reward + self.__discount_factor * maxQ - self.__qtable[self.__state][
                                                   action])

        self.__state = state
        self.__score += reward

    def best_action(self):
        best = None
        for a in self.__qtable[self.__state]:
            if not best \
                    or self.__qtable[self.__state][a] > self.__qtable[self.__state][best]:
                best = a
        return best
