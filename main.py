import yfinance as yf
import pandas as pd
import mplfinance as mpf

# msft = yf.Ticker("MSFT")
#
# # get stock info


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
    finance_service.load_history("AAPL", "2018-01-01", "2018-01-23")
    wallet_service = WalletService(wallet, finance_service)
    # TODO je sais pas quoi faire avec ce goal, comment on peut le définir ?
    # Si on met HIGH on ira jamais à Very High 😢
    goal = State.HIGH
    agent = Agent(wallet_service)

    ##while agent.state != goal:
    for i in range(8):
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
        print(agent.qtable)
