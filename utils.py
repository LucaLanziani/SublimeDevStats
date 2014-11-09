from __future__ import print_function, unicode_literals

import sublime

SETTINGS_FILE = 'DevStats.sublime-settings'


def log(*args):
    settings = sublime.load_settings(SETTINGS_FILE)
    if settings.get('debug', False):
        print(*args)


def log_exc(message):
    import sys
    exc = sys.exc_info()[1]
    log("%s" % exc)
    sublime.status_message("%s %s" % (message, exc))
