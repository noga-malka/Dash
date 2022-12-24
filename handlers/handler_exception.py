class DisconnectionEvent(Exception):
    def __init__(self, handler):
        self.message = f'The connection has been lost to handler: {handler}'

    def __str__(self):
        return self.message
