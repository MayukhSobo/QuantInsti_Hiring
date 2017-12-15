from time import sleep
from trading import helper
import threading
import csv
import os
from trading.constants import CURRENT_BUFFER
import numpy as np


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

            :param task_que: Universal Task Queue
            :return:
            """
        global CURRENT_BUFFER
        global lock
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
                    print(data)
                    CURRENT_BUFFER = data
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


    # def _run_trading_strategy(self):
    #     """
    #     Runs a trading strategy that
    #     is mentioned.
    #     :return:
    #     """
    #     pass

    def _validation(self, data):
        """
        Performs the validation of data
        fields. Protected method used only
        internally
        :return: Boolean ( successful data cleaning ?)
        """
        # Validating for numbers
        try:
            for index, value in enumerate(data[1::]):
                data[index] = float(value)
        except (ValueError, TypeError):
            # We can log the errors..Choosing the pass
            return False
        return True

    def run(self):
        """

        :return:
        """
        global CURRENT_BUFFER
        global lock
        while True:
            lock.acquire()
            if self.Q[0] == 'md-listener':
                self.Q.get()
                if self._validation(CURRENT_BUFFER):
                    self.buffer.append(np.array(CURRENT_BUFFER))
                    print(len(self.buffer))

            # self.Q.task_done()
            lock.release()
            sleep(4)

# def md_listen(task_que):
#     while True:
#         task_que.put('md-broadcast')
#         task_que.task_done()
#         sleep(4)


def om_listen(task_que):
    pass