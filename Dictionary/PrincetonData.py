from Tools.BaseData import BaseData

class PrincetonData(BaseData):
    def __init__(self) -> None:
        super().__init__()
        self._filename = "princetondata"
        self._compressEnabled = True

    def GetPrincetonMeanings(self, word):
        if self.IsInitialized():
            return self._GetItem(word.lower(), {})
        return None

    def AddPrincetonMeanings(self, word, princetonMeanins):
        if self.IsInitialized():
            self._SetItem(word.lower(), princetonMeanins)
