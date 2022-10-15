class Handler:
    def __init__(self):
        self.client = None
        self.connect()

    def connect(self):
        raise NotImplementedError()

    def disconnect(self):
        if self.client:
            self.client.close()
        self.client = None

    def read_line(self):
        raise NotImplementedError()
