from datetime import datetime, timedelta

from gui import StockFormView


class StockFormController:
    def __init__(self, view: StockFormView, interval: int = 14):
        self.view = view
        self.selected_date = ""
        self.view.validate_button.bind("<Button>", self.validate_date)
        self.interval = interval

        self.__is_start_date = True
        self.view.get_start_date_button.bind("<Button>", self.open_calendar_for_start_date)
        self.view.get_end_date_button.bind("<Button>", self.open_calendar_for_end_date)

        self.view.calender.bind("<<CalendarSelected>>", self.__date_selected)

    def open_calendar_for_start_date(self, _):
        print("open calender for start date")
        self.__is_start_date = True
        if self.view.end_date_value['text'] != 'Not yet':
            start_date = datetime.strptime(self.view.end_date_value['text'], '%Y-%m-%d')
            self.view.calender['maxdate'] = start_date - timedelta(days=1 + self.interval)
        self.view.show_calender()

    def open_calendar_for_end_date(self, _):
        self.__is_start_date = False
        if self.view.start_date_value['text'] != 'Not yet':
            start_date = datetime.strptime(self.view.start_date_value['text'], '%Y-%m-%d')
            self.view.calender['mindate'] = start_date + timedelta(days=1 + self.interval)
        self.view.show_calender()

    def validate_date(self, _):
        self.selected_date = self.view.calender.get_date()
        print(f"selection date : {self.selected_date}")

    def __date_selected(self, _):
        print(f"date selected : {self.view.calender.get_date()}")
        new_date = self.view.calender.get_date()
        if self.__is_start_date:
            self.view.update_start_date(new_date)
        else:
            self.view.update_end_date(new_date)
        self.view.hide_calender()
