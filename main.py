# Qu'est-ce que je veux déjà ??
# Déjà, je voudrais savoir comment on commente sur mac et avec quel raccourcis ?
# Ensuite, dans le cadre de notre projet, oui j'écris trop mais c'est aussi pour m'hbaituer à mon nouveau clavier
# Donc je disais du coup j'aiemerai avancer dans le cadre de mon projet de Trading
# Je dois faire la partie qui s'occupe de récupérer les données quoi
# Déjà on se base sur quelle monnaie ? USD va peut-être être le plus simple non ? Si
#   1. Prendre la valeur d'une action en USD entre deux dates voulues
#   2. Récupérer la valeur de toutes les minutes genre ça pourrait être pas mal

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
    # Et voilà le projet est terminé, et non, c'était une blague 🤡
