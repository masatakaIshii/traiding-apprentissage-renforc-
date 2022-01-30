import threading
from datetime import datetime, timedelta, date

from gui import StockFormView
from process import ProcessBot


class StockFormController:
    def __init__(self, view: StockFormView, process_bot: ProcessBot):
        self.view = view
        self.__selected_date = ""
        self.process_bot = process_bot

        self.__is_start_date = True
        self.__is_calendar_open = False

        self.view.get_start_date_button.bind("<Button>", self.open_calendar_for_start_date)
        self.view.get_end_date_button.bind("<Button>", self.open_calendar_for_end_date)

        yesterday = date.today() - timedelta(days=1)
        self.view.calendar['maxdate'] = yesterday
        self.view.calendar.bind("<<CalendarSelected>>", self.__date_selected)

    def open_calendar_for_start_date(self, _):
        self.__is_start_date = True
        self.__is_calendar_open = True
        self.view.show_calender()

    def open_calendar_for_end_date(self, _):
        self.__is_start_date = False
        self.__is_calendar_open = True
        self.view.show_calender()

    def __date_selected(self, _):
        new_date = self.view.calendar.get_date()
        if self.__is_start_date:
            self.view.update_start_date(new_date)
            self.view.get_start_date_button['text'] = 'Reset'
            self.view.get_start_date_button.bind("<Button>", self.__reset_start_and_end_date)
            start_date = datetime.strptime(new_date, '%Y-%m-%d')
            self.view.calendar['mindate'] = start_date + timedelta(days=1 + self.process_bot.get_interval())
        else:
            self.view.update_end_date(new_date)
            self.view.get_end_date_button['text'] = 'Reset'
            self.view.get_end_date_button.bind("<Button>", self.__reset_start_and_end_date)
            end_date = datetime.strptime(new_date, '%Y-%m-%d')
            self.view.calendar['maxdate'] = end_date - timedelta(days=1 + self.process_bot.get_interval())

        self.__is_calendar_open = False
        self.view.hide_calendar()

    def reset_form(self):
        self.view.stock_name_value.delete(0, 'end')
        yesterday = date.today() - timedelta(days=1)
        self.view.calendar['maxdate'] = yesterday
        self.__reset_start_and_end_date({})

    def __reset_start_and_end_date(self, _):
        if self.__is_calendar_open is True:
            self.view.hide_calendar()
        self.view.start_date_value['text'] = 'Not yet'
        self.view.get_start_date_button['text'] = 'Get date'
        self.view.get_start_date_button.bind("<Button>", self.open_calendar_for_start_date)
        self.view.calendar['mindate'] = None

        self.view.end_date_value['text'] = 'Not yet'
        self.view.get_end_date_button['text'] = 'Get date'
        self.view.get_end_date_button.bind("<Button>", self.open_calendar_for_end_date)
        self.view.calendar['maxdate'] = None

    def popup_output_validation(self, output: str, is_error: bool):
        self.view.output_validation['text'] = output
        threading.Thread(target=self.view.popup_output_validation).start()

    def get_stock_name(self):
        return self.view.stock_name_value.get()

    def get_start_date(self):
        return self.view.start_date_value['text']

    def get_end_date(self):
        return self.view.end_date_value['text']
