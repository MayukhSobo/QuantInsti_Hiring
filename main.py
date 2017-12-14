from trading import constants
from trading import preprocess
from trading import ex_server
import sys
from trading import porfolio
from multiprocessing import Process
from threading import Thread
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
    # server_process = Process(target=ex_server.run,
    #                          args=(server_port, ))
    # server_process.start()
    # server_process.join()
    # print('Server process pid: {}'.format(constants.EXCHANGE_SERVER_ID))
    # ex_server.run(port=server_port)
    ############################################
    # Create a portfolio
    account = porfolio.Porfolio(cash=1_000)
    # ############################################
    # Event Loop
    main_event(account)
    ############################################
    # Create thread workers and dispatch
    md_brd = MDBroadcast(name='md-broadcaster', que=constants.TASK_QUEUE)
    # md_lstn = Thread(target=md_listen, args=(constants.TASK_QUEUE,))
    # md_lstn.setDaemon(True)
    # md_lstn.start()
    # md_brd.setDaemon(True)
    md_brd.start()
    # Wait for all threads to end, practically forever..:)


if __name__ == "__main__":
    main()
