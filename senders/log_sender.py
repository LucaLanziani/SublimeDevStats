from SublimeDevStats.base_sender import Sender as BaseSender


class Sender(BaseSender):

    def __init__(self, endpoing):
        super(Sender, self).__init__(endpoing)

    def send(self, data):
        print(data)
