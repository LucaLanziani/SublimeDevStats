import sublime
import sublime_plugin
import urllib2
import json


def send_data(key):
    try:
        url = 'http://127.0.0.1:3000/keypress'
        data = json.dumps({"key": key})
        clen = len(data)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json', 'Content-Length': clen})
        f = urllib2.urlopen(req, timeout=0.01)
        print f.read()
    except Exception as e:
        print e


class TrackitCommand(sublime_plugin.TextCommand):

    def run(self, edit, key, command=None, args=None):
        send_data(key)
        if command is not None:
            self.view.run_command(command, args)
        else:
            for pos in self.view.sel():
                self.view.insert(edit, pos.begin(), key)
