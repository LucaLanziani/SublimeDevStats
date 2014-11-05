from __future__ import absolute_import, print_function

import json
import os

try:
    from .base_sender import Sender
    from ..utils import log, log_exc
except (ValueError, SystemError):
    from senders.base_sender import Sender
    from utils  import log, log_exc


class FileSender(Sender):

    def __init__(self, endpoint):
        super(FileSender, self).__init__(endpoint)
        self._endpoint = os.path.abspath(os.path.expanduser(self.endpoint))

    def send(self, data):
        data['timestamp'] = data['timestamp'].isoformat()
        data = json.dumps(data)
        try:
            with open(self._endpoint, 'a+') as fp:
                fp.write("%s\n" % data)
        except Exception:
            log_exc("SublimeDevStats can't write on %s because of" % self._endpoint)