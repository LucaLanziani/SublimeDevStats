import sublime
import sublime_plugin
import urllib2
import json
import time
import threading
import Queue


SETTINGS_FILE = 'Trackit.sublime-settings'
CommunicationQueue = Queue.Queue()

def send_data(filename, key, timestamp, url):
    try:
        data = json.dumps({"timestamp": timestamp, "filepath": filename, "key": key})
        clen = len(data)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json', 'Content-Length': clen})
        urllib2.urlopen(req, timeout=1)
    except Exception as e:
        sublime.status_message("%s while contacting %s" % (e, url))


class DevStatsSender(threading.Thread):

    def __init__(self, *args, **kwds):
        super(DevStatsSender, self).__init__(*args, **kwds)

    def run(self):
        msg = CommunicationQueue.get()
        while msg is not None:
            send_data(msg['filename'], msg['key'], msg['timestamp'], msg['url'])
            msg = CommunicationQueue.get()


class TrackitCommand(sublime_plugin.TextCommand):

    def run(self, edit, key, command=None, args=None):
        settings = sublime.load_settings(SETTINGS_FILE)
        endpoint = settings.get('endpoint')
        on_keypress = settings.get('on_keypress')
        filename = self.view.file_name()
        msg = {
            'filename': filename,
            'key': key,
            'timestamp': time.time(),
            'url': endpoint + on_keypress
        }
        CommunicationQueue.put(msg)
        if command is not None:
            self.view.run_command(command, args)
        else:
            for pos in self.view.sel():
                if pos.size() > 1:
                    self.view.erase(edit, pos)
                self.view.insert(edit, pos.begin(), key)

DevStatsSender().start()
