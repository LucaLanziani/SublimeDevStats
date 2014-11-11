import re

from SublimeDevStats.utils import log


class Blacklist(object):

    def __init__(self, re_list=None):
        regex_list = re_list or []
        self._setup(regex_list)

    def _setup(self, re_list):
        self._blacklist = self._unify_patterns(re_list)
        self.blacklisted_path = set()  # Cash of blacklisted paths
        self.allowed_paths = set()  # Cash of allowed path
        log(re_list, self._blacklist)

    def _unify_patterns(self, patterns):
        if patterns:
            expr = '^(%s)$' % '|'.join(patterns)
            return re.compile(expr)

    def _there_is_a_match(self, pathname):
        if self._blacklist.match(pathname) is not None:
            self.blacklisted_path.add(pathname)
            return True

        self.allowed_paths.add(pathname)
        return False

    def __contains__(self, pathname):

        if self._blacklist is None:
            return False
        elif pathname in self.allowed_paths:
            return False
        elif pathname in self.blacklisted_path:
            return True

        return self._there_is_a_match(pathname)


if __name__ == '__main__':
    pass
