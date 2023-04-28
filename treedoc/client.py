
class Client:
    def __init__(self, identificator):
        self.identificator = identificator
        self.local_counter = 0

    def inc(self):
        self.local_counter += 1
