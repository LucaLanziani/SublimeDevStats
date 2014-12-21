from __future__ import print_function

import threading
from datetime import datetime
from imp import load_source
from os.path import abspath, dirname, join
from sys import path

import sublime
import sublime_plugin

try:
    import queue
except ImportError:
    import Queue as queue

PLUGIN_DIR = abspath(join(dirname(__file__), '..'))

if PLUGIN_DIR not in path:
    path.append(PLUGIN_DIR)

from SublimeDevStats.utils import (CHAR_KEY_PREFIX, log, log_exc, SETTINGS_FILE,  # isort:skip
                                   THREAD_TIMEOUT)
from SublimeDevStats.utils.blacklist import Blacklist

class StatsSender(threading.Thread):

    def __init__(self, queue, *args, **kwds):
        super(StatsSender, self).__init__(*args, **kwds)
        self.settings = sublime.load_settings(SETTINGS_FILE)
        self.settings.clear_on_change('sender')
        self.settings.add_on_change('sender', self._reload_sender)
        self._reload_sender()
        self.queue = queue

    def _reload_sender(self):
        self.sender = None
        sender = self.settings.get('sender')
        endpoint = self.settings.get("%s_endpoint" % sender)
        try:
            sender_path = join(PLUGIN_DIR, 'SublimeDevStats/senders', '%s_sender.py' % (sender,))
            sender_module = load_source('sender', sender_path)
        except IOError:
            print("Can't find any module for %s sender" % sender)
        else:
            self.sender = sender_module.Sender(endpoint)

    def _get_data(self):
        try:
            data = self.queue.get(True, THREAD_TIMEOUT)
        except queue.Empty:
            data = None
        return data

    def run(self):
        data = self._get_data()
        while data is not None:
            if self.sender is not None:
                try:
                    self.sender.send(data)
                except Exception:
                    log_exc("Exception on send method")
            data = self._get_data()
        log("Terminating", threading.current_thread())


class DevTrackListener(sublime_plugin.EventListener):

    def __init__(self, *args, **kwargs):
        super(DevTrackListener, self).__init__(*args, **kwargs)
        self.settings = sublime.load_settings(SETTINGS_FILE)
        self.settings.clear_on_change('exclude')
        self.settings.add_on_change('exclude', self._reload_blacklist)
        self._reload_blacklist()
        self.communication_queue = queue.Queue()
        self.active_thread = None

    def _reload_blacklist(self):
        self.blacklist = Blacklist(self.settings.get('exclude'))

    def on_query_context(self, view, key, operator, operand, match_all):
        data = self._format_data(view, key, operand)
        self._send_data(data)
        return None

    def _check_thread(self):
        if self.active_thread is None or not self.active_thread.is_alive():
            self.active_thread = StatsSender(self.communication_queue)
            self.active_thread.start()
            log("Starting", self.active_thread)

    def _send_data(self, data):
        if data is not None:
            self._check_thread()
            self.communication_queue.put(data)

    def _format_data(self, view, key, operand):
        data = None
        filename = view.file_name()
        if key.endswith('_keypress') and filename is not None:
            keypress_type, _ = key.split('_')

            data = dict(
                filename=filename if filename not in self.blacklist else '',
                key=operand if keypress_type != CHAR_KEY_PREFIX else CHAR_KEY_PREFIX,
                timestamp=datetime.utcnow()
            )

        return data


class DevTrackCommand(sublime_plugin.TextCommand):

    def run(self, edit, key, command=None, args=None):
        pass
