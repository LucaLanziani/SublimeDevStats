from __future__ import print_function, absolute_import

import json
import os

from senders.base_sender import Sender as BaseSender
from utils  import log, log_exc


class Sender(BaseSender):

    def __init__(self, endpoint):
        super(Sender, self).__init__(endpoint)
        self._endpoint = os.path.abspath(os.path.expanduser(self.endpoint))

    def send(self, data):
        data['timestamp'] = data['timestamp'].isoformat()
        data = json.dumps(data)
        try:
            with open(self._endpoint, 'a+') as fp:
                fp.write("%s\n" % data)
        except Exception:
            log_exc("SublimeDevStats can't write on %s because of" % self._endpoint)