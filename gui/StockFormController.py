from gui import StockFormView


class StockFormController:
    def __init__(self, view: StockFormView):
        self.view = view
        self.selected_date = ""
        self.view.validate_button.bind("<Button>", self.validate_date)

    def validate_date(self, _):
        self.selected_date = self.view.calender.get_date()
        print(f"selection date : {self.selected_date}")


