from __future__ import print_function, absolute_import

import sublime

SETTINGS_FILE = 'DevStats.sublime-settings'


def log(*args):
    settings = sublime.load_settings(SETTINGS_FILE)
    if settings.get('debug'):
        print(*args)
