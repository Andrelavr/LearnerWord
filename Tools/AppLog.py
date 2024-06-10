from Tools.Singleton import Singleton

import logging

class AppLog(metaclass=Singleton):
    Dictionary = "Dictionary"
    FuncTime = "Function Time"
    WordsInBooks = "WordsInBooks"
    WordSearcher = "WordSearcher"
    CrosswordSystem = "CrosswordSystem"
    WordFilter = "WordFilter"

    def __init__(self) -> None:
        self._loggers = {}
        self._logfile = "Data/log"

    def InitListLoggers(self):
        self.SetEnableLogger(AppLog.Dictionary, False)
        self.SetEnableLogger(AppLog.FuncTime, False)
        self.SetEnableLogger(AppLog.WordsInBooks, False)
        self.SetEnableLogger(AppLog.WordSearcher, False)
        self.SetEnableLogger(AppLog.CrosswordSystem, False)
        self.SetEnableLogger(AppLog.WordFilter, False)
    
    def Log(self, name, message):
        logger = self._loggers.get(name, None)
        if logger:
            logger.log(logging.DEBUG, message)
    
    def SetEnableLogger(self, name, enable):
        if enable:
            self.EnableLogger(name)
        else:
            self.DisableLogger(name)
    
    def EnableLogger(self, name):
        if not name in self._loggers:
            self.InitLogger(name)
    
    def DisableLogger(self, name):
        if name in self._loggers:
            self._loggers.pop(name)
    
    def InitLogger(self, name):
        handler = logging.FileHandler(filename = self._logfile, mode = "a")
        handler.setLevel(logging.DEBUG)
        format = logging.Formatter('%(asctime)s,%(msecs)d %(name)s: %(message)s', "%H:%M:%S")
        handler.setFormatter(format)
        logger = logging.getLogger(name)
        logger.addHandler(handler)
        self._loggers[name] = logger
        self.Log(name, "Logger created")
