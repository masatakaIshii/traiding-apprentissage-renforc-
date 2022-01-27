import string
from typing import List

from gui.TradingView import TradingView
from logic.service.WalletService import WalletService


class TradingController:
    def __init__(self, wallet_service: WalletService, view: TradingView):
        self.__wallet_service = wallet_service
        self.__view = view

        self.__str_actions: List[string] = []

        self.__view.start_button.bind("<Button>", self.start)

    def start(self, _):
        self.__view.start_button_clicked()
        self.__view.start_button.unbind("<Button>")
        self.__view.pause_button.bind("<Button>", self.pause)

        print("controller start")

    def pause(self, _):
        self.__view.pause_button_clicked()
        self.__view.pause_button.unbind("<Button>")
        self.__view.start_button.bind("<Button>", self.start)
        print("controller pause")

    @property
    def str_actions(self):
        return self.__str_actions
