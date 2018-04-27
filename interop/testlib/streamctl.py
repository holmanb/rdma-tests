import sys


class Stdout():
    def __init__(self, default_stream):
        self._default = default_stream
    def on(self):
        sys.stdout = self._default
    def off(self):
        sys.stdout = open('/dev/null', 'w')


class Stderr():
    def __init__(self, default_stream):
        self._default = default_stream
    def on(self):
        sys.stderr = self._default
    def off(self):
        sys.stderr = open('/dev/null', 'w')

stdout = Stdout(sys.stdout)
stderr = Stdout(sys.stderr)
