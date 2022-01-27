import tkinter

import pandas

# # get stock info
from gui.TradingView import TradingView
from gui.TradingController import TradingController
from logic.Wallet import Wallet
from logic.service.WalletService import WalletService


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


# get historical market data
# hist = msft.history(interval="1d", start="2019-10-15", end="2021-10-15")
# # df = pd.DataFrame(hist)
# # + other methods etc.
from logic.FinanceService import FinanceService

if __name__ == '__main__':
    root = tkinter.Tk()
    trading_data = pandas.read_csv("resource/masa.csv", sep=';').set_index('Date')

    finance_service = FinanceService()
    finance_service.set_stock_history(trading_data)

    wallet_service = WalletService(wallet=Wallet(), finance_service=finance_service)

    root.minsize(720, 480)
    root.title("Trading bot")

    trading_view = TradingView(master=root)
    trading_controller = TradingController(wallet_service=wallet_service, view=trading_view),

    root.mainloop()

    # wallet = Wallet()

    # finance_service.load_history("AAPL", "2019-02-15", "2020-02-15")
    # # print(financeService.get_stock("2019-02-15", 20))
    # # print(financeService.get_interval_one_stock_history("2019-02-15", 33))
    # print(finance_service.stock_history)
    # print(finance_service.start_date)
    # print("------------------")
    # print(finance_service.get_interval_one_stock_history("2019-02-15", 20))
    #
    # wallet_service = WalletService(wallet, finance_service)
    # # TODO je sais pas trop quoi faire avec le goal
    # goal = State.VERY_HIGH
    # agent = Agent(wallet_service)
    # max = -10000
    # boucle = 1
    # ##while agent.state != goal:
    # for i in range(1000):
    #     print("")
    #     print(f"GRAND TOUR {i + 1}")
    #     agent.reset()
    #     count = 1
    #     for date, stock in finance_service.stock_history.iterrows():
    #         print("")
    #         print(f"TOUR {count}")
    #         print(f"DATE : {date} STOCK : {stock['Close']}")
    #         agent.current_date = date
    #         action = agent.best_action()
    #         print(f"BEST ACTION : {action}")
    #         agent.do_action(action)
    #         agent.update(action)
    #         print(f"STATE : {agent.state}")
    #         print(f"SCORE : {agent.score}")
    #         count += 1
    #
    #     if agent.score > max:
    #         max = agent.score
    #         boucle = i + 1
    #
    # print(f"MAX SCORE : {max} à la boucle {boucle}")
    #
    # print(pretty(agent.qtable))
# print(df)
# hist.where()['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
# print(hist.get('Close'))
#
#
# async def show_matplot():
#     print("show matplog")
#     mpf.plot(financeService.get_interval_one_stock_history("2019-02-15", 60), type="candle", volume=True, figratio=(
#         15, 7), style='yahoo', mav=(6, 15), title='spy candle charts')
#     for x in hist.get('Close'):
#         print(x)
# async def run_gui():
#     main_gui = Main()
#
#     main_gui.run()
# task1 = asyncio.create_task(show_matplot())
#
# task2 = asyncio.create_task(run_gui())
#
#
# await asyncio.gather(task2, task1)
