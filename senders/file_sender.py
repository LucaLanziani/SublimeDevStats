from __future__ import print_function, absolute_import

import os
import json
from .base_sender import Sender


class FileSender(Sender):

    def __init__(self, endpoint):
        super(FileSender, self).__init__(endpoint)
        self._endpoint = os.path.abspath(os.path.expanduser(self.endpoint))

    def send(self, data):
        data = json.dumps(data)
        with open(self._endpoint, 'a+') as fp:
            fp.write("%s\n" % data)
