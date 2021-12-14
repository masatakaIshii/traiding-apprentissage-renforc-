from logic.exceptions.StockNotFoundError import StockNotFoundError

class FinanceService:

    # Récupérer une action
    def get_stock(self, stock_name, date, amount):
        raise StockNotFoundError
