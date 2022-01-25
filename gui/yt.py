from datetime import datetime
from hashlib import new
import threading
from typing import Any
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import mplfinance as mpf
import plotly.graph_objects as go

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from kivy.properties import ObjectProperty

from logic.FinanceService import FinanceService
import time

# x = [1,2,3,4]
# y = [5,10,12,9]

# plt.plot(x,y)

# plt.ylabel("Y axis")
# plt.xlabel("X axis")

class Demo(FloatLayout):

    finance_service: FinanceService
    cur_date: datetime

    is_paused = False
    is_paused_label = ObjectProperty(None)
    timer_label = ObjectProperty(None)
    wallet_label = ObjectProperty(None)

    cur_timer = 0

    def __init__(self, finance_service: FinanceService,**kwargs):
        super().__init__(**kwargs)
        self.finance_service = finance_service
        start_date_str = self.finance_service.start_date
        if len(start_date_str) == 0:
            print("problem")
        else:
            self.cur_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            print(self.cur_date)
            self.update_timer_label()


    def update_timer_label(self):
        if self.is_paused:
            return
        self.thread_timer = threading.Timer(1.0, self.update_timer_label)
        self.cur_timer = self.cur_timer + 1
        self.thread_timer.start()
        cur_time = int(self.timer_label.text)
        self.timer_label.text = str(cur_time + 1)
   

    def press(self): 
        self.is_paused = not self.is_paused

        self.is_paused_label.text = "Is paused" if self.is_paused else "Is not paused"
        self.update_timer_label()
        self.show_matplot()

    def show_matplot(self):

        #self.cur_date = datetime.strptime(self.finance_service.start_date) +
        df = self.finance_service.get_interval_one_stock_history(self.finance_service.start_date, 60)
        print(df)

        # Problem data to set date : https://plotly.com/python/candlestick-charts/
        fig = go.Figure(data=[go.Candlestick(
                        open=df['Open'],
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'])])
        fig.show()


    def stop(self):
        self.is_paused = True
        self.update_timer_label()


class Main(App):

    demo_app: Demo
    finance_service: FinanceService

    def __init__(self, finance_service: FinanceService, **kwargs):
        super().__init__(**kwargs)
        self.finance_service = finance_service


    def build(self, ):
        Builder.load_file("./gui/layout_yt.kv")
        self.demo_app = Demo(finance_service=self.finance_service)
        return self.demo_app

    def on_stop(self):
        self.demo_app.stop()

