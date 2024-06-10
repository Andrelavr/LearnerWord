from Tools.DataReader import DataReader

from threading import Lock

class BaseData:

    def __init__(self) -> None:
        self._filename = "data"
        self._compressEnabled = False
        self._reader = None
        self._data = {}
        self._isDirtyData = False
        self._isInitialized = False
        self._threadLock = Lock()
    
    def Init(self):
        self._reader = DataReader(self._filename, self._compressEnabled)
        data = self._reader.Read()
        with self._threadLock:
            self._data = data
            if not self._data:
                self._data = {}
        self._isDirtyData = False
        self._isInitialized = True
    
    def Save(self):
        if self._isDirtyData:
            with self._threadLock:
                self._reader.Write(self._data)
                self._isDirtyData = False
    
    def SetDirty(self):
        self._isDirtyData = True
    
    def IsInitialized(self):
        return self._isInitialized
    
    def IsItemDataExist(self, item):
        return item in self._data
    
    def RemoveItem(self, key):
        if key in self._data:
            with self._threadLock:
                self._data.pop(key)
                self.SetDirty()
    
    def _GetValueByKey(self, item, valueKey, default = None):
        with self._threadLock:
            return self._data.get(item, dict()).get(valueKey, default)
    
    def _SetValueByKey(self, item, key, value):
        with self._threadLock:
            self._data.setdefault(item, dict())[key] = value
            self.SetDirty()
    
    def _GetItem(self, item, default):
        with self._threadLock:
            return self._data.get(item, default)
    
    def _SetItem(self, item, value):
        with self._threadLock:
            self._data[item] = value
            self.SetDirty()
