import tkinter
from tkinter import DISABLED, NORMAL

from bot.Action import Action


class TradingView(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)

        # Buttons
        buttons_container = tkinter.LabelFrame(self, padx=10, pady=10)
        self.start_button = tkinter.Button(buttons_container, text="Start")
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = tkinter.Button(buttons_container, text="Stop", state=DISABLED)
        self.stop_button.grid(row=0, column=2, padx=5, pady=5)
        buttons_container.pack(pady=10)

        # Wallet and Stock Container
        wallet_stocks_container = tkinter.LabelFrame(self, text="Wallet and stock information", padx=10, pady=10)

        # stock history container

        stock_history_container = tkinter.LabelFrame(wallet_stocks_container, text="Stock history information", pady=10,
                                                     padx=10)

        stock_index_label = tkinter.Label(stock_history_container, text="Stock index :")
        stock_index_label.grid(row=0, column=0)

        self.stock_index_value = tkinter.Label(stock_history_container, text="Default")
        self.stock_index_value.grid(row=0, column=1)

        self.stock_start_date_label = tkinter.Label(stock_history_container, text="Start date :")
        self.stock_start_date_label.grid(row=1, column=0)
        self.stock_start_date_value = tkinter.Label(stock_history_container, text="Not yet")
        self.stock_start_date_value.grid(row=1, column=1)

        self.stock_end_date_label = tkinter.Label(stock_history_container, text="End date :")
        self.stock_end_date_label.grid(row=2, column=0)
        self.stock_end_date_value = tkinter.Label(stock_history_container, text="Not yet")
        self.stock_end_date_value.grid(row=2, column=1)

        stock_history_container.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # Wallet container
        wallet_container = tkinter.LabelFrame(wallet_stocks_container, padx=10, pady=10)

        wallet_label = tkinter.Label(wallet_container, text="Wallet content :")
        wallet_label.grid(row=0, column=0)
        self.__wallet_amount = tkinter.Label(wallet_container, text="Not yet")
        self.__wallet_amount.grid(row=0, column=1)

        wallet_container.grid(row=1, column=0, pady=5, padx=5)

        # Date container
        date_container = tkinter.LabelFrame(wallet_stocks_container, padx=10, pady=10)

        date_label = tkinter.Label(date_container, text="Current date : ")
        date_label.grid(row=0, column=0)
        self.__date_content = tkinter.Label(date_container, text="Not yet")
        self.__date_content.grid(row=0, column=1)

        date_container.grid(row=1, column=1, pady=5, padx=5)

        # Stock information
        stock_infos_container = tkinter.LabelFrame(wallet_stocks_container, padx=10, pady=10)

        your_stock_label = tkinter.Label(stock_infos_container, text="Your stock value :")
        your_stock_label.grid(row=0, column=0)
        self.__your_stock_amount = tkinter.Label(stock_infos_container, text="Not stock amount yet")
        self.__your_stock_amount.grid(row=0, column=1)

        current_stock_label = tkinter.Label(stock_infos_container, text="Current stock value :")
        current_stock_label.grid(row=1, column=0)
        self.__current_stock_amount = tkinter.Label(stock_infos_container, text="Not current stock")
        self.__current_stock_amount.grid(row=1, column=1)

        stock_infos_container.grid(row=2, column=0, columnspan=2, pady=10)

        wallet_stocks_container.pack()

        # Historic
        historic_container = tkinter.LabelFrame(self, text=" Benefice Historic", padx=10, pady=10)

        self.__list_benefice = tkinter.Listbox(historic_container, width=30)
        self.__list_benefice.pack()

        historic_container.pack(pady=10)

        # Pack TradingView
        self.grid(row=0, column=0, rowspan=10, padx=10, pady=20)

    def start_button_clicked(self):
        self.start_button["state"] = DISABLED
        self.stop_button["state"] = NORMAL

    def stop_button_clicked(self):
        self.start_button["state"] = NORMAL
        self.stop_button["state"] = DISABLED

    def set_wallet_amount(self, wallet_amount: float):
        self.__wallet_amount["text"] = f"{str(wallet_amount)} €"

    def set_current_date(self, date: str):
        self.__date_content["text"] = date

    def set_your_stock_amount(self, stock_amount: float | None):
        self.__your_stock_amount["text"] = str(stock_amount) if stock_amount is not None else "Empty"

    def set_cur_stock_amount(self, stock_amount: float | None):
        self.__current_stock_amount["text"] = str(stock_amount) if stock_amount is not None else "Empty"

    def insert_benefice_in_list(self, benefice: float, date: str):
        self.__list_benefice.insert(0, f"{date}: Benefice is {benefice}")

    def update_stock_history(self, stock_index: str, start_date: str, end_date: str):
        self.stock_index_value['text'] = stock_index
        self.stock_start_date_value['text'] = start_date
        self.stock_end_date_value['text'] = end_date
