try:
	from .base_sender import Sender
except (ValueError, SystemError):
	from base_sender import Sender

class LogSender(Sender):

    def __init__(self, endpoing):
        super(LogSender, self).__init__(endpoing)

    def send(self, data):
        print(data)
