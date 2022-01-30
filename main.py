import tkinter

import pandas

from bot.Agent import Agent
from gui import QTableView, QTableController, StockFormView, StockFormController, BotConfigView, BotConfigController
from gui.TradingController import TradingController
from gui.TradingView import TradingView
from logic.FinanceService import FinanceService
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
    wallet = Wallet()
    finance_service = FinanceService(
        5)
    trading_data = pandas.read_csv("resource/masa.csv", sep=';').set_index('Date')

    finance_service.set_stock_history(trading_data)

    wallet_service = WalletService(wallet, finance_service)
    agent = Agent(wallet_service)
    print(finance_service.stock_history)

    process_bot = ProcessBot(finance_service, wallet_service, agent)

    root = tkinter.Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))
    stock_form_view = StockFormView(master=root)
    stock_form_controller = StockFormController(view=stock_form_view, process_bot=process_bot)

    qtable_view = QTableView(master=root)
    qtable_controller = QTableController(view=qtable_view)

    bot_config_view = BotConfigView(master=root)
    bot_config_controller = BotConfigController(view=bot_config_view, process_bot=process_bot)

    trading_view = TradingView(master=root)
    trading_controller = TradingController(
        view=trading_view,
        qtable_controller=qtable_controller,
        stock_form_controller=stock_form_controller,
        bot_config_controller=bot_config_controller,
        process_bot=process_bot)

    root.title("Trading bot")
    root.mainloop()
