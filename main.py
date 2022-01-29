from datetime import datetime

from bot.Action import Action
from bot.Agent import Agent
from logic.FinanceService import FinanceService
from logic.Wallet import Wallet
from logic.service.WalletService import WalletService
import threading
import tkinter

import pandas

# # get stock info
from gui.TradingView import TradingView
from gui.TradingController import TradingController
from logic.Wallet import Wallet
from logic.service.WalletService import WalletService
from process import ProcessBot


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


if __name__ == '__main__':
    # root = tkinter.Tk()
    # trading_data = pandas.read_csv("resource/masa.csv", sep=';').set_index('Date')

    #finance_service = FinanceService()
    #
    # wallet_service = WalletService(wallet=Wallet(), finance_service=finance_service)
    #
    # trading_view = TradingView(master=root)
    # trading_controller = TradingController(master=root, wallet_service=wallet_service, view=trading_view),

    wallet = Wallet()
    finance_service = FinanceService(
        5)  # 50 - 38 / 38 - 26 / 26 - 14 / 14 - 2 / 2 -10 / 10 - 22 / 22 - 34 / 34 - 48 / +
    trading_data = pandas.read_csv("resource/masa.csv", sep=';').set_index('Date')

    finance_service.set_stock_history(trading_data)
    # start_date = "2019-07-01"
    # end_date = "2020-07-01"
    # finance_service.load_history("MCD", start_date, end_date)
    wallet_service = WalletService(wallet, finance_service)
    agent = Agent(wallet_service)
    print(finance_service.stock_history)

    interval = 14

    process_bot = ProcessBot(finance_service, wallet_service, agent)

    root = tkinter.Tk()
    trading_view = TradingView(master=root)
    trading_controller = TradingController(master=root, view=trading_view, process_bot=process_bot)


    # for i in range(5):
    #
    #     finance_service.define_current_interval("2018-12-31",
    #                                             interval)  # 14 premiers jours donc je peux faire calcul moyenne
    #     agent.current_date = str(finance_service.current_interval.last_valid_index())
    #     while agent.current_date:
    #         # print(f"CURRENT DATE : {agent.current_date}")
    #
    #         for i in range(interval):
    #             agent.current_date = finance_service.next_date(agent.current_date)  # on est sur la date d'après
    #             if not agent.current_date:
    #                 break
    #             # print(f"CURRENT DATE : {agent.current_date}")
    #             action = agent.best_action()
    #             # print(f"BEST ACTION : {action}")
    #             maybe_stock_bought = wallet_service.get_stock(0)
    #             # if action is Action.BUY:
    #             #     maybe_stock_bought = None
    #             agent.do_action(action)
    #             agent.update(action, maybe_stock_bought)
    #             # print(f"STATE : {agent.state}")
    #             # print(f"SCORE : {agent.score}")
    #         finance_service.define_current_interval(str(finance_service.current_interval.last_valid_index()), interval)
    #
    # pretty(agent.qtable)
