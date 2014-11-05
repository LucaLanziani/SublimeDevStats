from __future__ import print_function

import calendar
import json
import threading

import sublime

try:
    from ..utils import log
    from .http_sender import HttpSender
except (ValueError, SystemError):
    from utils import log
    from http_sender import HttpSender

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2


class InfluxdbSender(HttpSender):

    def _format_data(self):
        return json.dumps([{
            "name" : "devstats",
            "columns" : ["time", "filename", "key"],
            "points" : [
                [
                    calendar.timegm(data['timestamp'].utctimetuple()),
                    data['filename'],
                    data['key']
                ] for data in self.data
            ]
        }])
