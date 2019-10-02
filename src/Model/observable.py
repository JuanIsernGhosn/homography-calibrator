class Observable:
    def __init__(self, data):
        self.data = data
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callbacks[func]

    def _doAllCallbacks(self):
        for func in self.callbacks:
            func(self.data)

    def set(self, data, callbacks=True):
        self.data = data
        if callbacks:
            self._doAllCallbacks()

    def get(self):
        return self.data

    def unset(self):
        self.data = None