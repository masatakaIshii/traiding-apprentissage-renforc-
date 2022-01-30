import tkinter
from tkinter import ttk, CENTER, W, END

from bot import Action


class QTableView(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)

        qtable_label = tkinter.Label(self, text="QTable content")
        qtable_label.pack()

        self.table = ttk.Treeview(self)
        self.table['columns'] = ("Action.BUY", "Action.KEEP", "Action.SELL")

        # Format columns
        self.table.column("#0", width=120, minwidth=25)
        self.table.column("Action.BUY", anchor=CENTER, width=120)
        self.table.column("Action.KEEP", anchor=CENTER, width=120)
        self.table.column("Action.SELL", anchor=CENTER, width=120)

        # Heading
        self.table.heading("#0", text="Node info", anchor=W)
        self.table.heading("Action.BUY", text="Action BUY", anchor=W)
        self.table.heading("Action.KEEP", text="Action KEEP", anchor=W)
        self.table.heading("Action.SELL", text="Action SELL", anchor=W)

        self.count = 0
        self.table.pack(pady=20, expand=True, fill='y')

        self.grid(row=1, column=1, rowspan=7, padx=10, pady=10, sticky="ns")

    def build_qtable(self, qtable: dict, parent_id: int | None):
        concerned_parent_id = '' if parent_id is None else parent_id

        for key, value in qtable.items():
            item_id = self.count
            if isinstance(value, dict):
                values = ['', '', '']
                if Action.BUY in value.keys():
                    values = [cur_val for cur_key, cur_val in value.items()]
                self.table.insert(parent=f"{concerned_parent_id}", index='end', iid=f'{item_id}',
                                  text=f'{key}',
                                  values=values, open=True)
                self.count += 1
                if values[0] == '':
                    self.build_qtable(value, item_id)

    def remove_all_qtable(self):
        for child in self.table.get_children():
            self.table.delete(child)
