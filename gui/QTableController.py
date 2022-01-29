from gui import QTableView


class QTableController:
    def __init__(self, view: QTableView):
        self.view = view

    def update_qtable(self, qtable: dict):
        self.view.build_qtable(qtable=qtable, parent_id=None)

    def reset_qtable(self):
        self.view.remove_all_qtable()
