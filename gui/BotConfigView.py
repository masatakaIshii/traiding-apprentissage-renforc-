import tkinter

from bot import Action


class BotConfigView(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        # Bot container
        bot_container = tkinter.LabelFrame(self, text="Bot information", padx=10, pady=10)

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

        self.grid(row=0, column=1, padx=10, pady=5)

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
