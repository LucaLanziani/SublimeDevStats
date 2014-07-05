import sublime
import sublime_plugin
import urllib2
import json

SETTINGS_FILE = 'Trackit.sublime-settings'


def send_data(key, url):
    try:
        data = json.dumps({"key": key})
        clen = len(data)
        req = urllib2.Request(url, data, {'Content-Type': 'application/json', 'Content-Length': clen})
        f = urllib2.urlopen(req, timeout=0.01)
        print f.read()
    except Exception as e:
        print "%s while contacting %s" % (e, url)


class TrackitCommand(sublime_plugin.TextCommand):

    def run(self, edit, key, command=None, args=None):
        settings = sublime.load_settings(SETTINGS_FILE)
        endpoint = settings.get('endpoint')
        on_keypress = settings.get('on_keypress')
        send_data(key, endpoint + on_keypress)
        if command is not None:
            self.view.run_command(command, args)
        else:
            for pos in self.view.sel():
                self.view.insert(edit, pos.begin(), key)
