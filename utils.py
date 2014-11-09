from __future__ import print_function, absolute_import, unicode_literals

import sublime
from os.path import abspath, dirname, join

PROJECT_ROOT = abspath(join(dirname(__file__)))

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
