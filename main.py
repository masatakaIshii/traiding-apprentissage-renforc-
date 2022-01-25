import json

import yfinance as yf
import pandas as pd
import mplfinance as mpf
from gui.yt import Main


# msft = yf.Ticker("MSFT")
#
# # get stock info
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
from bot.Agent import Agent
from bot.State import State
from logic.FinanceService import FinanceService
from logic.Wallet import Wallet
from logic.service.WalletService import WalletService

if __name__ == '__main__':
    wallet = Wallet()
    finance_service = FinanceService()
    finance_service.load_history("AAPL", "2019-02-15", "2020-02-15")
    # print(financeService.get_stock("2019-02-15", 20))
    # print(financeService.get_interval_one_stock_history("2019-02-15", 33))
    print(finance_service.stock_history)
    print(finance_service.start_date)
    print("------------------")
    print(finance_service.get_interval_one_stock_history("2019-02-15", 20))

    wallet_service = WalletService(wallet, finance_service)
    # TODO je sais pas trop quoi faire avec le goal
    goal = State.VERY_HIGH
    agent = Agent(wallet_service)
    max = -10000
    boucle = 1
    ##while agent.state != goal:
    for i in range(1000):
        print("")
        print(f"GRAND TOUR {i + 1}")
        agent.reset()
        count = 1
        for date, stock in finance_service.stock_history.iterrows():
            print("")
            print(f"TOUR {count}")
            print(f"DATE : {date} STOCK : {stock['Close']}")
            agent.current_date = date
            action = agent.best_action()
            print(f"BEST ACTION : {action}")
            agent.do_action(action)
            agent.update(action)
            print(f"STATE : {agent.state}")
            print(f"SCORE : {agent.score}")
            count += 1

        if agent.score > max:
            max = agent.score
            boucle = i + 1

    print(f"MAX SCORE : {max} à la boucle {boucle}")

    print(pretty(agent.qtable))
# print(df)
# hist.where()['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
# print(hist.get('Close'))

    main_gui = Main(finance_service)

    main_gui.run()

        # async def show_matplot():
        #     print("show matplog")
        #     mpf.plot(financeService.get_interval_one_stock_history("2019-02-15", 60), type="candle", volume=True, figratio=(
        #         15, 7), style='yahoo', mav=(6, 15), title='spy candle charts')
        #     for x in hist.get('Close'):
        #         print(x)
        # async def run_gui():
        #     main_gui = Main()

        #     main_gui.run()
        # task1 = asyncio.create_task(show_matplot())

        # task2 = asyncio.create_task(run_gui())


        # await asyncio.gather(task2, task1)

