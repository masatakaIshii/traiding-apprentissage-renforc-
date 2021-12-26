# Dans l'agent, il doit y avoir:
# - qtable
# - best_action
# - discount factor
# - learning rate
# - update avec les rewards
# - les rewards du coup lol
REWARD_VERY_HIGH = 1000
REWARD_HIGH = 500
REWARD_LITTLE_HIGH = 200
REWARD_LITTLE_LOW = -200
REWARD_LOW = -500
REWARD_VERY_LOW = -1000

ACTIONS = [BUY, KEEP, SELL]


# Quel sera notre environnement finalement ?
#
class Agent:
    def __init__(self, environment, learning_rate=1, discount_factor=0.5):
        # environnement -> notre partie logique je pense ?
        # il nous faudra au moins le portefeuille
        self.__learning_rate = learning_rate
        self.__discount_factor = discount_factor
        self.__environment = environment
        self.__qtable = {}
        # TODO voir comment implémenter la qtable
        # for s in self.__environment.states:
        #     self.__qtable[s] = {}
        #     for a in ACTIONS:
        #         self.__qtable[s][a] = 0.0
        self.reset()

    # TODO IMPLEMENT
    # Update sert à mettre à jour l'état, le score et la qtable
    def update(self, state, action, reward):
        return

    # TODO IMPLEMENT
    # Best action sert à trouver la meilleure action à faire
    # En fonction de notre état et de notre Qtable
    def best_action(self):
        return

    def reset(self):
        self.__state = self.__environment.start
        self.__score = 0
