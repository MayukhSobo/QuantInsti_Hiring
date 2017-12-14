from time import sleep
from trading import helper
import threading
import csv
import os


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
            # next(stock_data)
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
        while True:
            # Keep on polling until 'exit' event
            if self.Q[0] != 'md-broadcast':
                # Don't bother for other tasks
                continue
            else:
                a = self.Q.get()
                # If it is md-broadcast task
                data = next(self.data)
                if data == ['line-end']:
                    self.Q.put('exit')
                else:
                    print(data)
                    self.Q.put('md-listener')
                    self.Q.put('md-broadcast')
            self.Q.task_done()
            sleep(5)


class MDListener(threading.Thread):
    def __init__(self, que, name):
        super(self.__class__, self).__init__()
        self.name = name
        self.Q = que
        self.buffer = None

def md_listen(task_que):
    while True:
        task_que.put('md-broadcast')
        task_que.task_done()
        sleep(4)


def om_listen(task_que):
    pass