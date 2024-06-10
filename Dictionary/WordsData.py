from Dictionary.WordsDataKeys import WordsDataKeys
from Tools.BaseData import BaseData

class WordsData(BaseData):

    def __init__(self) -> None:
        super().__init__()
        self._filename = "wordsdata"

    def GetMeanings(self, word):
        return self._GetValueByKey(word, WordsDataKeys.Meaning, "")

    def GetTranscription(self, word):
        return self._GetValueByKey(word, WordsDataKeys.Transcription, "")
    
    def GetWordList(self):
        return list(self._data.keys())
    
    def AddWord(self, word, transcription, meaning):
        newdata = {}
        newdata[WordsDataKeys.Meaning] = meaning
        newdata[WordsDataKeys.Transcription] = transcription
        self._data[word] = newdata
        self.SetDirty()
    
    def UpdateTranscription(self, word, transcription):
        if not self.IsItemDataExist(word):
            return
        if transcription and transcription != self.GetTranscription(word):
            self._data[word][WordsDataKeys.Transcription] = transcription
            self.SetDirty()
    
    def UpdateMeaning(self, word, meaningList):
        if not self.IsItemDataExist(word):
            return
        currentMeanings = self.GetMeanings(word)
        for meaning in meaningList:
            if meaning not in currentMeanings:
                self._data[word][WordsDataKeys.Meaning].append(meaning)
                self.SetDirty()

class GameData(BaseData):

    KeyNumOfGames = 'games'
    KeyNumOfWrongAns = 'fails'
    KeyLastLenWinSeries = 'series'
    KeyLastGame = 'time'
    KeyCurrentWordLevel = 'level'

    def __init__(self) -> None:
        super().__init__()
        self._filename = "gamedata"
        self._compressEnabled = True

    def GetNumOfGames(self, word):
        return self._GetValueByKey(word, GameData.KeyNumOfGames, 0)

    def GetNumOfWrongAns(self, word):
        return self._GetValueByKey(word, GameData.KeyNumOfWrongAns, 0)
    
    def GetLastWinSeries(self, word):
        return self._GetValueByKey(word, GameData.KeyLastLenWinSeries, 0)
    
    def GetLastGameTime(self, word):
        return self._GetValueByKey(word, GameData.KeyLastGame, 0)
    
    def GetLevel(self, word):
        return self._GetValueByKey(word, GameData.KeyCurrentWordLevel, 0)
    
    def Update(self, word, numOfGames = -1, numOfWrongAns = -1, winSeries = -1, lastTime = -1, level = -1):
        if not self.IsItemDataExist(word):
            self._data[word] = {}
        self._UpdateGameValue(word, GameData.KeyNumOfGames, numOfGames)
        self._UpdateGameValue(word, GameData.KeyNumOfWrongAns, numOfWrongAns)
        self._UpdateGameValue(word, GameData.KeyLastLenWinSeries, winSeries)
        self._UpdateGameValue(word, GameData.KeyLastGame, lastTime)
        self._UpdateGameValue(word, GameData.KeyCurrentWordLevel, level)
        self.SetDirty()
    
    def _UpdateGameValue(self, word, key, value):
        if value >= 0:
            self._data[word][key] = value
