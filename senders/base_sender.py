

class Sender(object):

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def send(self, *args, **kwds):
        raise NotImplementedError()
