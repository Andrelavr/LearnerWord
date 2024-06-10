from Tools.ThreadManager import ThreadManager

class BaseDataDownloader:
    def __init__(self) -> None:
        self._data = None
        self._text = ""
        self._callback = None

    def InitData(self):
        if self._data:
            ThreadManager().RunNewThread("initdownloader", self._data.Init, self._OnInitialized)
    
    def Save(self):
        if self._data:
            self._data.Save()
    
    def Download(self, text, callback):
        if not text:
            return
        self._text = text
        self._callback = callback
        if not self._IsDataInitialized():
            return
        ThreadManager().RunNewThread("download", self._Downloading, self._OnDownloading)
    
    def _OnDownloading(self):
        if self._callback:
            self._callback()

    def _IsDataInitialized(self):
        if not self._data:
            return False
        return self._data.IsInitialized()

    def _OnInitialized(self):
        if self._text:
            self.Download(self._text, self._callback)
