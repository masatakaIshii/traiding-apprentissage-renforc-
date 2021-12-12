import yfinance as yf
import pandas as pd
import mplfinance as mpf

msft = yf.Ticker("MSFT")

# get stock info


# get historical market data
hist = msft.history(interval="1d", start="2021-09-15", end="2021-10-15")

# + other methods etc.
if __name__ == '__main__':
    # print(hist.get('Close'))

    mpf.plot(hist, type="candle", volume=True, figratio=(
        15, 7), style='yahoo', mav=(6, 15), title='spy candle charts')
    # for x in hist.get('Close'):
    #     print(x)
