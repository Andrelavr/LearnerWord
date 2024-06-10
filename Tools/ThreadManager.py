from Tools.Singleton import Singleton
from Tools.ThreadWorker import ThreadWorker

from threading import Event
from threading import get_native_id

class ThreadData:
    def __init__(self, thread, finishEvent, callback) -> None:
        self.thread = thread
        self.finishEvent = finishEvent
        self.callback = callback

class ThreadManager(metaclass=Singleton):
    def __init__(self):
        self._threads = []

    def RunNewThread(self, name, func, callback) -> ThreadWorker:
        finishEvent = Event()
        thread = ThreadWorker(func, name, finishEvent)
        thread.start()
        self._threads.append(ThreadData(thread, finishEvent, callback))
        return thread

    def Update(self):
        if not self._threads:
            return
        updatedThreads = []
        for data in self._threads:
            if data.finishEvent.is_set():
                data.callback()
            else:
                updatedThreads.append(data)
        self._threads = updatedThreads
    
    def GetThreadId(self):
        return get_native_id()
