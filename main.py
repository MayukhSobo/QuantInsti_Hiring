from trading import constants
from trading import preprocess
# from trading import ex_server
from subprocess import Popen
import sys
from trading import porfolio
from trading.workers import *


def main_event(account):
    if constants.TASK_QUEUE.empty():
        # First task in chain is always independent
        constants.TASK_QUEUE.put('md-broadcast')
    else:
        event = constants.TASK_QUEUE.get()
        if event in constants.EVENT_QUEUE_ID:
            print(account)
            sys.exit()


def main(server_port=8080):
    # Load the data from Quandl
    ############################################
    print('----- Gathering Data from Quandl ------')
    stock = preprocess.Gather('APPLE',
                              constants.API_KEY,
                              '2012-01-01',
                              '2017-12-15')
    ############################################
    # Create a dataset
    stock.write_csv('./trading/data/stock_data.csv')
    ############################################

    # Start the dummy exchange server
    # print('----- Starting the EXCHANGE server ------')
    # server = Popen(['python', 'server.py'])
    # stdout_data, stderr_data = server.communicate()
    # print(stdout_data)
    ############################################
    # Create a portfolio

    account = porfolio.Porfolio(cash=1_000,
                                p_file='./trading/data/portfolio.csv')
    ############################################
    # Event Loop
    main_event(account)
    ############################################
    # Create thread workers and dispatch
    md_brd = MDBroadcast(name='md-broadcaster', que=constants.TASK_QUEUE)
    md_lstn = MDListener(name='md-listener', que=constants.TASK_QUEUE)
    om_lstn = OMListener(name='om-listener', que=constants.TASK_QUEUE, portfolio=account)
    # md_lstn = Thread(target=md_listen, args=(constants.TASK_QUEUE,))
    # md_lstn.setDaemon(True)
    # md_lstn.start()
    # md_brd.setDaemon(True)
    md_brd.start()
    md_lstn.start()
    om_lstn.start()

    # Wait for all threads to end, practically forever..:)


if __name__ == "__main__":
    main(server_port=8081)
