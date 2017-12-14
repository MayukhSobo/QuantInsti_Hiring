from time import sleep


def md_broadcast(task_que):
    """
    This checks for 'md_broadcast' event
    in the event queue and if it comes the
    read one line of the CSV file and broadcast
    it to the MD-Listener. It also pushes the
    'md-listener' event to the task event queue.

    :param task_que: Universal Task Queue
    :return:
    """
    pass


def md_listen(task_que):
    pass


def om_listen(task_que):
    pass