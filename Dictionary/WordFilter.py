from Tools.AppLog import AppLog

class WordFilter:
    AnyItem = '*'
    ForbiddenItem = '#'

    def __init__(self) -> None:
        self.CleanFilter()
    
    def CleanFilter(self):
        self._start = ""
        self._center = ""
        self._end = ""
        self._minLen = 0
        self._maxLen = 0
        self._centerIndex = 0
        self._ignore = []
    
    def SetLen(self, max, min = 1):
        self._minLen = min
        self._maxLen = max
    
    def AddIgnore(self, item):
        AppLog().Log(AppLog.WordFilter, "AddIgnore. item = {0}".format(item))
        self._ignore.append(item)
    
    def SetFilter(self, filterStr, index):
        AppLog().Log(AppLog.WordFilter, "SetFilter. filter = {0} ind = {1}".format(filterStr, index))
        if index >= len(filterStr):
            return
        self._maxLen = len(filterStr)
        self._start = filterStr[:index]
        self._end = filterStr[index + 1:]
        self._center = filterStr[index]
    
    def GetCenterIndex(self):
        return self._centerIndex

    def CheckWord(self, word):
        AppLog().Log(AppLog.WordFilter, "CheckWord. word = {0}".format(word))
        if len(word) < self._minLen or len(word) > self._maxLen:
            return False
        if word in self._ignore:
            return False
        if not self._center:
            return True
        self._centerIndex = -1
        while(True):
            self._centerIndex = word.find(self._center, self._centerIndex + 1)
            if self._centerIndex == -1:
                return False
            else:
                if self._CheckCharacters(word):
                    return True

    def _CheckCharacters(self, word):
        if self._centerIndex > len(self._start) or (len(word) - self._centerIndex - 1) > len(self._end):
            return False
        exWord = WordFilter.AnyItem + word + WordFilter.AnyItem
        exIndex = self._centerIndex + 1
        for ch, f in zip(exWord[exIndex - 1::-1], self._start[::-1]):
            if not self._CheckChar(ch, f):
                return False
        for ch, f in zip(exWord[exIndex + 1:], self._end):
            if not self._CheckChar(ch, f):
                return False
        return True
    
    def _CheckChar(self, wordCh, filterCh):
        if filterCh == WordFilter.AnyItem:
            return True
        elif filterCh == WordFilter.ForbiddenItem:
            return False
        else:
            if wordCh == WordFilter.AnyItem:
                return False
            if wordCh.lower() == filterCh.lower():
                return True
        return False
