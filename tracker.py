import sublime
import sublime_plugin
import urllib2
import json
import time
import threading
import Queue
import os


SETTINGS_FILE = 'Trackit.sublime-settings'
CommunicationQueue = Queue.Queue()


def send_http(filename, key, timestamp, url):
    try:
        data = json.dumps({"timestamp": timestamp, "filepath": filename, "key": key})
        clen = len(data)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json', 'Content-Length': clen})
        urllib2.urlopen(req, timeout=1)
    except Exception as e:
        sublime.status_message("%s while contacting %s" % (e, url))


def write_file(filename, key, timestamp, filepath):
    _filepath = os.path.abspath(os.path.expanduser(filepath))
    with open(_filepath, 'a+') as fp:
        fp.write("%s,%s,%s\n" % (filename, key, timestamp))


class DevStatsSender(threading.Thread):

    def __init__(self, *args, **kwds):
        super(DevStatsSender, self).__init__(*args, **kwds)

    def run(self):
        msg = CommunicationQueue.get()
        settings = sublime.load_settings(SETTINGS_FILE)
        while msg is not None:
            if settings.get('sender') == "http":
                endpoint = settings.get('endpoint')
                send_http(msg['filename'], msg['key'], msg['timestamp'], endpoint)
            else:
                filepath = settings.get('filepath')
                write_file(msg['filename'], msg['key'], msg['timestamp'], filepath)
            msg = CommunicationQueue.get()


class TrackitListener(sublime_plugin.EventListener):

    def on_query_context(self, view, key, operator, operand, match_all):
        print "key: %r" % [key, operator, operand, match_all]
        filename = view.file_name()
        msg = {
            'filename': filename,
            'key': operand,
            'timestamp': time.time()
        }
        CommunicationQueue.put(msg)
        return None


class TrackitCommand(sublime_plugin.TextCommand):

    def run(self, edit, key, command=None, args=None):
        pass

DevStatsSender().start()
