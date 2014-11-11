import re, logging, json, hashlib
import cPickle as pickle


class Blacklist():

    def __init__(self, dirs=[], files=[], contains=[], extentions=[]):
        super(Blacklist, self).__init__()

        expr = self._unify_escaped(escaped)
        compiled = re.compile(expr)
        self._blacklist = set([compiled])
        self.blacklisted_path = set()  # Cash of blacklisted paths
        self.allowed_paths=set()  # Cash of allowed path

    def _unify_patterns(self, patterns):
        patterns = filter(lambda e: e is not None, patterns)
        if len(patterns) == 0: return None

        expr ='^(%s)$' % '|'.join(patterns)
        return expr

    def _check_match(self, pattern, pathname):
        return pattern.match(pathname) is not None

    def is_blacklisted(self, pathname):

        if pathname in self.blacklisted_path:
            return True

        matches = map(lambda p: self._check_match(p, pathname),self._blacklist)

        if reduce(lambda x, y: x or y, matches, False):
            self.blacklisted_path.add(pathname)
            return True
        else:
            self.allowed_paths.add(pathname)
            return False


if __name__ == '__main__':
    pass