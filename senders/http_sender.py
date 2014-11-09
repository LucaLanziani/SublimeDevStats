from __future__ import print_function

import json
import threading

import sublime
from SublimeDevStats.senders.base_sender import Sender as BaseSender
from SublimeDevStats.utils import log_exc

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


class Sender(BaseSender):

    def __init__(self, *args):
        super(Sender, self).__init__(*args)
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
        sublime.set_timeout(self._send, 5000)

    def _format_data(self):
        data = [
            dict(
                filename=data['filename'],
                key=data['key'],
                timestamp=data['timestamp'].isoformat()
            ) for data in self.data
        ]
        return json.dumps(data)

    def _get_data(self):
        with self.data_lock:
            data = self._format_data()
            self.data = []
        return data

    def _add_data(self, data):
        with self.data_lock:
            if not self.data:
                self._set_send_timeout()
            self.data.append(data)

    def _send(self):
        if self.data:
            data = self._get_data()
            headers = {'Content-Type': 'application/json', 'Content-Length': len(data)}
            self.http.post(self.endpoint, data=data, headers=headers)

    def send(self, data):
        self._add_data(data)

    def post(self, url, data=None, headers=None):
        encoded = data.encode('utf-8')
        req = urllib2.Request(url, encoded, headers)
        try:
            urllib2.urlopen(req, timeout=1)
        except Exception:
            log_exc("SublimeDevStat can send data to %s because" % url)
