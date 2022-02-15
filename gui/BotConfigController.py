from bot import Action
from bot.Agent import Agent
from gui import BotConfigView
from process import ProcessBot


class BotConfigController:
    def __init__(self, view: BotConfigView, process_bot: ProcessBot):
        self.__view = view
        self.__process_bot = process_bot

        interval = self.__process_bot.get_interval()
        self.update_interval(interval)
        self.__view.interval_entry.insert(0, interval)
        self.__view.interval_save_btn.bind("<Button>", self.set_new_interval)

        nb_categories = self.__process_bot.finance_service.category_number
        self.update_nb_categories(nb_categories)
        self.__view.nb_categories_entry.insert(0, nb_categories)
        self.__view.nb_categories_save_btn.bind("<Button>", self.set_new_nb_categories)

        learning_rate = self.__process_bot.agent.learning_rate
        self.update_learning_rate(learning_rate)
        self.__view.learning_rate_entry.insert(0, learning_rate)
        self.__view.learning_rate_save_btn.bind("<Button>", self.set_new_learning_rate)

        discount_factor = self.__process_bot.agent.discount_factor
        self.update_discount_factor(discount_factor)
        self.__view.discount_factor_entry.insert(0, discount_factor)
        self.__view.discount_factor_save_btn.bind("<Button>", self.set_discount_factor)

        iteration = self.__process_bot.iteration
        self.update_iteration(iteration)
        self.__view.iteration_entry.insert(0, iteration)
        self.__view.iteration_save_btn.bind("<Button>", self.set_iteration)

    def update_action(self, action: Action):
        self.__view.update_action_labels_depend_to_action(action=action)

    def update_interval(self, interval: int):
        self.__view.interval_value['text'] = f"{interval}"

    def update_nb_categories(self, nb_categories: int):
        self.__view.nb_categories_value['text'] = f"{nb_categories}"

    def update_learning_rate(self, learning_rate: float):
        self.__view.learning_rate_value['text'] = f"{round(learning_rate, 2)}"

    def update_discount_factor(self, discount_factor: float):
        self.__view.discount_factor_value['text'] = f"{round(discount_factor, 2)}"

    def update_iteration(self, iteration: int):
        self.__view.iteration_value['text'] = f"{iteration}"

    def set_new_interval(self, _):
        new_interval = int(self.__view.interval_entry.get())
        self.__process_bot.set_interval(new_interval)
        self.update_interval(self.__process_bot.get_interval())

    def set_new_nb_categories(self, _):
        self.__process_bot.finance_service.category_number = int(self.__view.nb_categories_entry.get())
        self.update_nb_categories(self.__process_bot.finance_service.category_number)

    def set_new_learning_rate(self, _):
        self.__process_bot.agent.learning_rate = float(self.__view.learning_rate_entry.get())
        self.update_learning_rate(self.__process_bot.agent.learning_rate)

    def set_discount_factor(self, _):
        self.__process_bot.agent.discount_factor = float(self.__view.discount_factor_entry.get())
        self.update_discount_factor(self.__process_bot.agent.discount_factor)

    def set_iteration(self, _):
        self.__process_bot.iteration = int(self.__view.iteration_entry.get())
        self.update_iteration(self.__process_bot.iteration)
