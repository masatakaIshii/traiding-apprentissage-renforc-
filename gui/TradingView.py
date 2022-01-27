import tkinter
from tkinter import DISABLED, NORMAL


class TradingView(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.__is_start = False

        self.start_button = tkinter.Button(text="Start", command=self.start_button_clicked)
        self.start_button.pack(pady=10)

        self.pause_button = tkinter.Button(text="Pause", command=self.pause_button_clicked, state=DISABLED)
        self.pause_button.pack(pady=10)

        self.pack()

    def start_button_clicked(self):
        self.__is_start = True
        self.start_button["state"] = DISABLED
        self.pause_button["state"] = NORMAL

    def pause_button_clicked(self):
        self.__is_start = False
        self.start_button["state"] = NORMAL
        self.pause_button["state"] = DISABLED
