from bot import Action
from gui import BotConfigView


class BotConfigController:
    def __init__(self, view: BotConfigView):
        self.__view = view

    def update_action(self, action: Action):
        self.__view.update_action_labels_depend_to_action(action=action)
