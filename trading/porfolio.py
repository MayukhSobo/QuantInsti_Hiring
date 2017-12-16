import csv
import os


class Porfolio:
    """
    Creates a portfolio of a user
    """
    def __init__(self, cash, p_file, n_stocks=0):
        self._cash = cash
        self.portfolio_file = p_file
        self._stocks = n_stocks
        with open(self.portfolio_file, 'w') as p_file:
            csv_writer = csv.writer(p_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['timestamp', 'portfolio_value'])

    def __str__(self):
        print('You have: ${} remaining'.format(self.cash))

    def get_portfolio_value(self, current_price):
        return self.cash + self.stocks * current_price

    def write_portfolio_value(self, timestamp, current_price):
        with open(self.portfolio_file, 'a') as p_file:
            csv_writer = csv.writer(p_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([str(timestamp),
                                self.get_portfolio_value(current_price)])

    def sell(self, cp, n_stocks):
        if n_stocks == '*' and self.stocks > 0:
            self._cash += cp * self.stocks
            self._stocks = 0
        else:
            # // TODO Need to implement later
            pass

    def buy(self, cp, n_amount):
        if n_amount == '*' and self.cash >= cp:
            can_buy = int(self.cash / cp)
            self._stocks += can_buy
            self._cash -= cp * can_buy

    @property
    def cash(self):
        return self._cash

    @property
    def stocks(self):
        return self._stocks
