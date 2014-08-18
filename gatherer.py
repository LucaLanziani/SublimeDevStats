import sublime
import sublime_plugin
import urllib2
import json
import time
import threading
import Queue
import os


SETTINGS_FILE = 'DevStats.sublime-settings'
CommunicationQueue = Queue.Queue()


class Sender(object):

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def send(self, *args, **kwds):
        raise NotImplementedError()


class HttpSender(Sender):

    def send(self, msg):
        data = json.dumps(msg)
        clen = len(data)
        req = urllib2.Request(self.endpoint, data, {'Content-Type': 'application/json', 'Content-Length': clen})
        try:
            urllib2.urlopen(req, timeout=1)
        except Exception as e:
            sublime.status_message("%s while contacting %s" % (e, self.endpoint))


class FileSender(Sender):

    def __init__(self, endpoint):
        super(FileSender, self).__init__(endpoint)
        self._endpoint = os.path.abspath(os.path.expanduser(self.endpoint))

    def send(self, msg):
        data = json.dumps(msg)
        try:
            with open(self._endpoint, 'a+') as fp:
                fp.write("%s\n" % data)
        except Exception as e:
            Sublime.status_message("%s while writing %s" % (e, self._endpoint))

class LogSender(Sender):

    def __init__(self, endpoing):
        super(LogSender, self).__init__(endpoing)

    def send(self, msg):
        data = json.dumps(msg)
        print(data)


class StatsSender(threading.Thread):

    senders = {
        "http": HttpSender,
        "file": FileSender,
        "log": LogSender,
        None: LogSender
    }

    def __init__(self, *args, **kwds):
        super(StatsSender, self).__init__(*args, **kwds)
        settings = sublime.load_settings(SETTINGS_FILE)
        sender = settings.get('sender')
        self.sender_class = self.senders.get(sender)
        if self.sender_class is not None:
            self.sender = self.sender_class(settings.get('senders', {}).get(sender, {}).get('endpoint'))

    def run(self):
        msg = CommunicationQueue.get()
        while msg is not None:
            if self.sender is not None:
                self.sender.send(msg)
            msg = CommunicationQueue.get()


class DevTrackListener(sublime_plugin.EventListener):

    def on_query_context(self, view, key, operator, operand, match_all):
        if key.endswith('_keypress'):
            msg = {
                'filename': view.file_name(),
                'key': 'char',
                'timestamp': time.time()
            }
            
            keypress_type, _ = key.split('_')
            if keypress_type != 'char':
                msg['key'] = operand

            CommunicationQueue.put(msg)
        return None


class DevTrackCommand(sublime_plugin.TextCommand):

    def run(self, edit, key, command=None, args=None):
        pass

StatsSender().start()
