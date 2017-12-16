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

    def __str__(self):
        print('You have: ${} remaining'.format(self.cash))

    def get_portfolio_value(self, current_price):
        return self.cash + self.stocks * current_price

    def write_portfolio_value(self, timestamp, current_price):
        with open(self.portfolio_file, 'a') as p_file:
            csv_writer = csv.writer(p_file, delimiter=',',
                                   quotechar='|',
                                   quoting=csv.QUOTE_MINIMAL)
            if not os.path.exists(self.portfolio_file):
                csv_writer.writerow(['timestamp', 'portfolio_value'])
            csv_writer.writerow([str(timestamp),
                                self.get_portfolio_value(current_price)])



    @property
    def cash(self):
        return self._cash

    @property
    def stocks(self):
        return self._stocks
