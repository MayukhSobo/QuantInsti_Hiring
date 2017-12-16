from time import sleep
import threading
import csv
from datetime import datetime as dt
import numpy as np
import requests
import json

lock = threading.Lock()


class MDBroadcast(threading.Thread):
    def __init__(self, que, name=None):
        super(self.__class__, self).__init__()
        self.name = name
        self.Q = que
        self._data = self._get_csv_line()

    @property
    def data(self):
        return self._data

    def _get_csv_line(self):
        with open('./trading/data/stock_data.csv', 'r') as stock_data:
            next(stock_data)
            for each_stock in csv.reader(stock_data):
                # Generator for parsing long CSV without memory issue
                yield each_stock

    def run(self):
        """
            This checks for 'md_broadcast' event
            in the event queue and if it comes the
            read one line of the CSV file and broadcast
            it to the MD-Listener. It also pushes the
            'md-listener' event to the task event queue.
            :return:
            """
        global CURRENT_DATA_BUFFER
        global lock
        # i = 0
        while True:
            # Keep on polling until 'exit' event
            # if self.Q[0] != 'md-broadcast':
            #     # Don't bother for other tasks
            #     continue
            lock.acquire()
            if self.Q[0] == 'md-broadcast':
                self.Q.get()
                # If it is md-broadcast task
                data = next(self.data)
                if data == ['line-end']:
                    self.Q.put('exit')
                else:
                    # i += 1
                    # print(data, i)
                    CURRENT_DATA_BUFFER = data
                    self.Q.put('md-listener')
                    # Only 'md-broadcast' can register itself
                    self.Q.put('md-broadcast')
            # self.Q.task_done()
            lock.release()
            sleep(5)


class MDListener(threading.Thread):
    def __init__(self, que, name):
        super(self.__class__, self).__init__()
        self.name = name
        self.Q = que
        self.buffer = []

    def SMA_LMA(self, ns:int, data: np.ndarray) -> tuple:
        """
        This implements the actual trading strategy
        algorithm. This method should be kept as simple
        as possible. This calculates the Long term and
        Short term moving averages and then performs the
        following operations. Total number of data points
        are taken for long term moving averages and hence
        we should keep the data as clean as possible. This
        method is a private method and should not be called
        directly. A wrapper called _run_trading_strategy()
        should be used as it perform the memory cleaning
        stuffs before hand.

        SMA - Short Term Moving Average
        LMA - Long Term Moving Average

        If SMA < LMA  ⇒ sell all stocks
        If SMA > LMA  ⇒ buy the stocks, using all the cash that you’ve
        :param ns: Number of data points for SMA
        :return: ('SELL', nStocks) or ('BUY', nAmount)
        """
        closing_prices = data[:, 1].astype(float)
        LMA = closing_prices.mean()
        SMA = closing_prices[-ns:].mean()
        if SMA < LMA:
            return 'SELL', '*'
        else:
            return 'BUY', '*'

    def _run_trading_strategy(self, strategy='sma-lma', **kwargs):
        """
        Runs a trading strategy that is mentioned.
        By default it is SMA-LMA
        :return:
        """
        if strategy == 'sma-lma':
            # // TODO Need to outsource this function instead of being method of class
            ns = kwargs.get('ns', 5)
            nl = kwargs.get('nl', 10)
            if len(self.buffer) > nl:
                while len(self.buffer) != nl:
                    self.buffer.pop(0)

            if len(self.buffer) == nl:
                data = np.asarray(self.buffer)
                # print(data)
                return self.SMA_LMA(ns, data)

            if len(self.buffer) < nl:
                # Can not do anything until we have at least nl data points
                print(f'Not enough data to run the strategy.\n\tRequired {nl} data points '
                      f'\n\tEncountered {len(self.buffer)} data points')
                return

    def _validation(self, data):
        """
        Performs the validation of data
        fields. Protected method used only
        internally
        :return: Boolean ( successful data cleaning ?)
        """
        # Validating for numbers
        try:
            for index, value in enumerate(data[1::], start=1):
                data[index] = float(value)
        except (ValueError, TypeError):
            # We can log the errors..Choosing the pass
            return False, None
        return True, data

    def run(self):
        """

        :return:
        """
        global CURRENT_DATA_BUFFER
        global CURRENT_DECISION_BUFFER
        global lock
        while True:
            lock.acquire()
            if self.Q[0] == 'md-listener':
                self.Q.get()
                valid, data = self._validation(CURRENT_DATA_BUFFER)
                if valid:
                    self.buffer.append(np.array(data))
                    decision = self._run_trading_strategy(strategy='sma-lma', ns=5, nl=10)
                    if decision:
                        # print(decision)
                        CURRENT_DECISION_BUFFER = decision
                        self.Q.put('om-listener')
            lock.release()
            sleep(4)

# def md_listen(task_que):
#     while True:
#         task_que.put('md-broadcast')
#         task_que.task_done()
#         sleep(4)


# def om_listen(task_que):
#     pass

class OMListener(threading.Thread):
    def __init__(self, que, portfolio, name=None):
        super(self.__class__, self).__init__()
        self.name = name
        self.Q = que
        self.portfolio = portfolio

    @staticmethod
    def _create_order(port):
        """
        It sends the order to the server
        and receives the order id from the
        exchange server.
        :param: port address of exchange server
        :return: Order Status
        """
        url = f'http://localhost:{port}'
        order_id = requests.post(url + '/order').text
        oid = json.loads(json.loads(order_id))['order_id']
        return requests.get(url + f'/order/:{oid}').text
        # return order_id

    def run(self):
        """
            :return:
            """
        global CURRENT_DECISION_BUFFER
        global CURRENT_DATA_BUFFER
        global lock

        while True:
            lock.acquire()
            if self.Q[0] == 'om-listener':
                self.Q.get()
                decision = CURRENT_DECISION_BUFFER[0]
                amount = CURRENT_DECISION_BUFFER[1]
                # cp = CURRENT_DECISION_BUFFER[2]
                last_closed_value = float(CURRENT_DATA_BUFFER[-1])
                order_status = None
                if decision in ['BUY', 'SELL']:
                    # Send the request to the exchange server
                    order_status = OMListener._create_order(port=8080)
                if order_status == 'True':
                    if decision == 'SELL':
                        # If we are selling stocks
                        self.portfolio.sell(cp=last_closed_value, n_stocks=amount)
                    elif decision == 'BUY':
                        # If we are buying stocks
                        self.portfolio.buy(cp=last_closed_value, n_amount=amount)
                # Write the portfolio value to the CSV file
                self.portfolio.write_portfolio_value(timestamp=dt.now(),
                                                     current_price=last_closed_value)
            lock.release()
            sleep(5)