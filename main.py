from datetime import datetime
from bot.Agent import Agent
from logic.FinanceService import FinanceService
from logic.Wallet import Wallet
from logic.service.WalletService import WalletService


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
        8)  # 50 - 38 / 38 - 26 / 26 - 14 / 14 - 2 / 2 -10 / 10 - 22 / 22 - 34 / 34 - 48 / +
    start_date = "2019-01-01"
    end_date = "2020-01-01"
    finance_service.load_history("AAPL", start_date, end_date)
    wallet_service = WalletService(wallet, finance_service)
    agent = Agent(wallet_service)

    interval = 14
    finance_service.define_current_interval("2019-01-01 00:00:00",
                                            interval)  # 14 premiers jours donc je peux faire calcul moyenne
    agent.current_date = str(finance_service.current_interval.last_valid_index())
    while agent.current_date:
        print(f"CURRENT DATE : {agent.current_date}")

        for i in range(interval):
            agent.current_date = finance_service.next_date(agent.current_date)  # on est sur la date d'après
            if not agent.current_date:
                break
            print(f"CURRENT DATE : {agent.current_date}")
            action = agent.best_action()
            print(f"BEST ACTION : {action}")
            agent.do_action(action)
            agent.update(action)
            print(f"STATE : {agent.state}")
            print(f"SCORE : {agent.score}")
        finance_service.define_current_interval(str(finance_service.current_interval.last_valid_index()), interval)

    #
    # max = -10000
    # boucle = 1
    # ##while agent.state != goal:
    # for i in range(100):
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
