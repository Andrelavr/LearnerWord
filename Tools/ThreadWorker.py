from threading import Thread

class ThreadWorker(Thread):
    def __init__(self, workFunc, name, finishEvent, daemonWorker = True):
        Thread.__init__(self, daemon = daemonWorker)
        self.name = name
        self._workFunc = workFunc
        self._finishEvent = finishEvent

    def run(self):
        self._workFunc()
        self._finishEvent.set()
