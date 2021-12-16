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
from logic.FinanceService import FinanceService

financeService = FinanceService()
financeService.load_history("AAPL", "2018-02-15", "2020-02-15")

if __name__ == '__main__':
    print(financeService.get_stock("2019-02-15", 20))
    #print(financeService.stock_history.loc["2018-02-15"]['Close'])
    #print(financeService.stock_history.loc["2018-02-15"])
# print(hist.index[0])
# print(hist.loc["2019-10-15"])


# print(df)
# hist.where()['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
# print(hist.get('Close'))
#
# mpf.plot(hist, type="candle", volume=True, figratio=(
#     15, 7), style='yahoo', mav=(6, 15), title='spy candle charts')
# # for x in hist.get('Close'):
# #     print(x)
