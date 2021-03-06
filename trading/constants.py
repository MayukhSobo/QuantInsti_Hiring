from trading import helper

API_KEY = "rfJexxxWCSDzmyE7Qn_d"

COMPANIES = {
    "APPLE": "WIKI/AAPL"
}

EVENT_QUEUE_ID = {
    'md-broadcaster',  # For market data broadcast
    'md-listener',  # For market data listener
    'om-listener',  # For Order Manager Listener
    'exit'  # Exit the system
}

TASK_QUEUE = helper.IndexedQueue()
EXCHANGE_SERVER_ID = None
CURRENT_DATA_BUFFER = None
CURRENT_DECISION_BUFFER = None
