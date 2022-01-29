from bot import Action


class ProcessData:
    def __init__(self, current_action: Action, current_date: str):
        self.action = current_action
        self.date = current_date
