import sys

from trading import constants
from trading import porfolio
from trading import preprocess
from trading.workers import *


def main_event(account):
    if constants.TASK_QUEUE.empty():
        # First task in chain is always independent
        constants.TASK_QUEUE.put('md-broadcaster')
    else:
        event = constants.TASK_QUEUE.get()
        if event in constants.EVENT_QUEUE_ID:
            print(account)
            sys.exit()


def main(capital, data_path):

    if data_path.split('/')[-1] == 'stock_data.csv':
        # Load the data from Quandl
        ############################################
        print('----- Gathering Data from Quandl ------')
        stock = preprocess.Gather('APPLE',
                                  constants.API_KEY,
                                  '2012-01-01',
                                  '2017-12-15')
        ############################################
        # Create a data set
        stock.write_csv(data_path)
        ############################################

    # Create a portfolio
    account = porfolio.Porfolio(cash=capital,
                                p_file='./trading/data/portfolio.csv')
    ############################################
    # Event Loop
    main_event(account)
    ############################################
    # Create thread workers and dispatch
    md_broadcast = MDBroadcast(name='md-broadcaster', que=constants.TASK_QUEUE, data_path=data_path, portfolio=account)
    md_listen = MDListener(name='md-listener', que=constants.TASK_QUEUE)
    om_listen = OMListener(name='om-listener', que=constants.TASK_QUEUE, portfolio=account)
    md_broadcast.start()
    md_listen.start()
    om_listen.start()

    # Wait for all threads to end, practically forever..:)


if __name__ == "__main__":
    cap = float(sys.argv[1])
    dp = './trading/data/stock_data.csv'
    try:
        dp = './trading/data/' + sys.argv[2]
    except IndexError:
        pass
    main(capital=cap, data_path=dp)
