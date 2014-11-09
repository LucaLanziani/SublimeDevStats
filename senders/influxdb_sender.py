from __future__ import print_function

import calendar
import json

from SublimeDevStats.senders.http_sender import Sender as HttpSender

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2  # noqa


class Sender(HttpSender):

    def _format_data(self):
        return json.dumps([{
            "name": "devstats",
            "columns": ["time", "filename", "key"],
            "points": [
                [
                    calendar.timegm(data['timestamp'].utctimetuple()),
                    data['filename'],
                    data['key']
                ] for data in self.data
            ]
        }])
