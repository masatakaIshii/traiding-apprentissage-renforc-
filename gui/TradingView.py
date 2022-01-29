import tkinter
from tkinter import DISABLED, NORMAL

from bot.Action import Action


class TradingView(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)

        # Buttons
        buttons_container = tkinter.LabelFrame(master, padx=10, pady=10)
        self.start_button = tkinter.Button(buttons_container, text="Start")
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = tkinter.Button(buttons_container, text="Stop", state=DISABLED)
        self.stop_button.grid(row=0, column=2, padx=5, pady=5)
        buttons_container.pack(pady=10)

        # Wallet and Stock Container
        wallet_stocks_container = tkinter.LabelFrame(master, text="Wallet and stock information", padx=10, pady=10)

        # Wallet container
        wallet_container = tkinter.LabelFrame(wallet_stocks_container, padx=10, pady=10)

        wallet_label = tkinter.Label(wallet_container, text="Wallet content :")
        wallet_label.grid(row=0, column=0)
        self.__wallet_amount = tkinter.Label(wallet_container, text="Not yet")
        self.__wallet_amount.grid(row=0, column=1)

        wallet_container.grid(row=0, column=0, pady=5, padx=5)

        # Date container
        date_container = tkinter.LabelFrame(wallet_stocks_container, padx=10, pady=10)

        date_label = tkinter.Label(date_container, text="Current date : ")
        date_label.grid(row=0, column=0)
        self.__date_content = tkinter.Label(date_container, text="Not yet")
        self.__date_content.grid(row=0, column=1)

        date_container.grid(row=0, column=1, pady=5, padx=5)

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

        stock_infos_container.grid(row=1, column=0, columnspan=2, pady=5)

        wallet_stocks_container.pack()

        # Bot container
        bot_container = tkinter.LabelFrame(master, text="Bot information", padx=10, pady=10)

        # Count bot iteration
        count_bot_container = tkinter.LabelFrame(bot_container, padx=10, pady=10)
        iteration_bot_label = tkinter.Label(count_bot_container, text="Iteration :")
        iteration_bot_label.grid(row=0, column=0)
        self.__iteration_bot_value = tkinter.Label(count_bot_container, text="Not yet")
        self.__iteration_bot_value.grid(row=0, column=1)

        count_bot_container.grid(row=0)

        action_container = tkinter.LabelFrame(bot_container, text="Actions", padx=10, pady=10)
        self.__action_buy = tkinter.Label(action_container, text="BUY", fg="#0f0", bg="#fff")
        self.__action_buy.grid(row=0, column=0, padx=10, pady=5)

        self.__action_keep = tkinter.Label(action_container, text="KEEP", fg="#555", bg="#fff")
        self.__action_keep.grid(row=0, column=1, padx=10, pady=5)

        self.__action_sell = tkinter.Label(action_container, text="SELL", fg="#00f", bg="#fff")
        self.__action_sell.grid(row=0, column=2, padx=10, pady=5)

        action_container.grid(row=1, column=0)

        bot_container.pack(pady=10)

        # Historic
        historic_container = tkinter.LabelFrame(master, text="Historic", padx=10, pady=10)

        list_benefice_container = tkinter.LabelFrame(historic_container, padx=10, pady=10)

        list_benefice_label = tkinter.Label(list_benefice_container, text="Benefices")
        list_benefice_label.grid(row=0, column=0)
        self.__list_benefice = tkinter.Listbox(list_benefice_container, width=30)
        self.__list_benefice.grid(row=1, column=0)

        list_benefice_container.grid(row=0, column=0)

        historic_container.pack()

        # Pack TradingView
        self.pack()

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

    def set_count_bot_iter(self, count: int):
        self.__iteration_bot_value["text"] = str(count)

    def update_action_labels_depend_to_action(self, action):
        self.__reset_action_labels()
        match action:
            case Action.BUY:
                self.__action_buy["fg"] = "#fff"
                self.__action_buy["bg"] = "#0f0"
            case Action.KEEP:
                self.__action_keep["fg"] = "#fff"
                self.__action_keep["bg"] = "#555"
            case Action.SELL:
                self.__action_sell["fg"] = "#fff"
                self.__action_sell["bg"] = "#00f"
            case _:
                return

    def __reset_action_labels(self):
        self.__action_buy["fg"] = "#0f0"
        self.__action_buy["bg"] = "#fff"

        self.__action_keep["fg"] = "#555"
        self.__action_keep["bg"] = "#fff"

        self.__action_sell["fg"] = "#00f"
        self.__action_sell["bg"] = "#fff"

    def insert_benefice_in_list(self, benefice: float, date: str):
        self.__list_benefice.insert(0, f"{date}: Benefice is {benefice}")
