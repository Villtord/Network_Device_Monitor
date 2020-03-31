"""
Definition of new class of repeated timer which repeats any "function"
passed to it with given "interval". Can be used in any general class
in contrast to the QTimer object.
"""
from threading import Timer


class RepeatedTimer(object):
    def __init__(self, interval, function, *args):
        self._timer = None
        self.function = function
        self.interval = interval
        self.args = args
        self.is_running = False

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

