from __future__ import print_function, absolute_import

import sublime
import threading
import json

try:
    from ..utils import log
    from .senders.base_sender import Sender
except (ValueError, SystemError):
    from utils import log
    from senders.base_sender import Sender

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


class HttpSender(Sender):

    def __init__(self, *args):
        super(HttpSender, self).__init__(*args)
        self.__init_http_sender()

    def __init_http_sender(self):
        try:
            import requests
            self.http = requests
        except ImportError:
            self.http = self
        self.data_lock = threading.Lock()
        self.data = []
        self._set_send_timeout()

    def _set_send_timeout(self):
        log(threading.current_thread())
        sublime.set_timeout(self._send, 5000)

    def _get_json_data(self):
        with self.data_lock:
            data = json.dumps(self.data)
            self.data = []
        return data

    def _add_data(self, data):
        with self.data_lock:
            if not self.data:
                self._set_send_timeout()
            self.data.append(data)

    def _send(self):
        if self.data:
            data = self._get_json_data()
            headers = {'Content-Type': 'application/json', 'Content-Length': len(data)}
            self.http.post(self.endpoint, data=data, headers=headers)

    def send(self, data):
        self._add_data(data)

    def post(self, url, data=None, headers=None):
        encoded = data.encode('utf-8')
        req = urllib2.Request(url, encoded, headers)
        urllib2.urlopen(req, timeout=1)
