import tkinter

from tkcalendar import Calendar


class StockFormView(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)

        self.calender_container = tkinter.LabelFrame(self, text="Fetch new stock")

        self.validate_button = tkinter.Button(self.calender_container, text="Validate")
        self.validate_button.grid(row=0, pady=10)

        calender_title = tkinter.Label(self.calender_container, text="Calender title")
        calender_title.grid(row=0, column=1)
        self.calender = Calendar(self.calender_container, selectmode="day", year=2020, month=5, day=22,
                                 date_pattern='y-mm-dd')
        self.calender.grid(row=1, column=1, pady=5, padx=20)

        self.calender_container.pack()

        self.grid(row=0, column=1, columnspan=3, padx=10, pady=5)

        # self.calender_container.grid_remove()
