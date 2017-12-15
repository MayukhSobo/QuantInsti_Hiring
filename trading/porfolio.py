
class Porfolio:
    """
    Creates a portfolio of a user
    """
    def __init__(self, cash, n_stocks=0):
        self.cash = cash
        self.stocks = n_stocks

    def __str__(self):
        print('You have: ${} remaining'.format(self.cash))

    def get_portfolio_value(self, current_price):
        return self.cash + self.stocks * current_price
