import time
import tkinter

from tkcalendar import Calendar


class StockFormView(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)

        fetch_stock_container = tkinter.LabelFrame(self, text="Fetch new stock")

        # Stock form
        stock_form_container = tkinter.LabelFrame(fetch_stock_container)

        stock_name_label = tkinter.Label(stock_form_container, text="Stock name :")
        stock_name_label.grid(row=0, column=0)
        self.stock_name_value = tkinter.Entry(stock_form_container)
        self.stock_name_value.grid(row=0, column=1)

        start_date_label = tkinter.Label(stock_form_container, text="Start date :")
        start_date_label.grid(row=1, column=0)
        self.start_date_value = tkinter.Label(stock_form_container, text="Not yet")
        self.start_date_value.grid(row=1, column=1)
        self.get_start_date_button = tkinter.Button(stock_form_container, text="Get date")
        self.get_start_date_button.grid(row=1, column=2)

        end_date_label = tkinter.Label(stock_form_container, text="End date :")
        end_date_label.grid(row=2, column=0)
        self.end_date_value = tkinter.Label(stock_form_container, text="Not yet")
        self.end_date_value.grid(row=2, column=1)
        self.get_end_date_button = tkinter.Button(stock_form_container, text="Get date")
        self.get_end_date_button.grid(row=2, column=2)

        self.validate_button = tkinter.Button(stock_form_container, text="Validate")
        self.validate_button.grid(row=3, columnspan=3, pady=10)

        self.output_validation = tkinter.Label(stock_form_container)

        stock_form_container.grid(row=0, column=0)

        self.calender_container = tkinter.LabelFrame(fetch_stock_container)

        self.calender_title = tkinter.Label(self.calender_container, text="Calender title")
        self.calender_title.grid(row=0, column=1)

        self.calendar = Calendar(self.calender_container, selectmode="day", year=2020, month=5, day=22,
                                 date_pattern='y-mm-dd')
        self.calendar.grid(row=1, column=1, pady=5, padx=20)
        # self.calender_container.grid(row=0, column=1)

        fetch_stock_container.pack()

        self.grid(row=0, column=1, columnspan=3, padx=10, pady=5)

        # self.calender_container.grid_remove()

    def show_calender(self):
        self.calender_container.grid(row=0, column=1)

    def hide_calendar(self):
        self.calender_container.grid_remove()

    def update_start_date(self, start_date: str):
        self.start_date_value['text'] = start_date

    def update_end_date(self, end_date: str):
        self.end_date_value['text'] = end_date

    def popup_output_validation(self):
        self.output_validation.grid(row=4, columnspan=3, pady=10)
        time.sleep(3)
        self.output_validation.grid_remove()
        self.output_validation['text'] = ''
