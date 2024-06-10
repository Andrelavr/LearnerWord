from Dictionary.Level import Level

import random
import time

class WordData:
    def __init__(self, word = "", time = 0):
        self.word = word
        self.time = time

class WordOrderManager:
    def __init__(self) -> None:
        self._data = {}
        self._data[Level.LevelNewWords] = []
        self._data[Level.LevelInTraining] = []
        self._data[Level.LevelLearned] = []
        self._data[Level.LevelIgnore] = []
        self._justTrained = []
        self._wordsToChoose = []
        self._insertRangeForRepeat = (5, 15)
        self._lenOfChunk = 100
        self._numOfWinToLevelUp = 5
        self._delayAfterTrain = 6 * 60 * 60
    
    def SetWord(self, word, level, seriesOfWin = 0, time = 0):
        if level not in self._data:
            level = Level.LevelInTraining
        if self._IsDelayNeeded(seriesOfWin, time) and level != Level.LevelIgnore:
            self._justTrained.append(WordData(word, time))
        else:
            self._data[level].append(WordData(word, time))
    
    def GetNextWord(self):
        if len(self._wordsToChoose) == 0:
            return "***"
        return self._GetWordByIndex()
    
    def GetNextWordByFilter(self, filter):
        if len(self._wordsToChoose) == 0:
            return None
        for ind, word in enumerate(reversed(self._wordsToChoose)):
            if filter(word):
                return self._GetWordByIndex(len(self._wordsToChoose) - ind - 1)
        return None
    
    def RepeatWord(self, word):
        ind = 0
        if word in self._wordsToChoose:
            self._wordsToChoose.remove(word)
        if len(self._wordsToChoose) > self._insertRangeForRepeat[0]:
            rand = random.randint(self._insertRangeForRepeat[0], min(len(self._wordsToChoose), self._insertRangeForRepeat[1]))
            ind = max(0, len(self._wordsToChoose) - rand)
        self._wordsToChoose.insert(ind, word)
    
    def RemoveWord(self, word):
        if word in self._wordsToChoose:
            self._wordsToChoose.remove(word)
    
    def SetNewLevel(self, word, level):
        if level == Level.LevelIgnore:
            if word in self._wordsToChoose:
                self._wordsToChoose.remove(word)
        else:
            self.RepeatWord(word)
    
    def InitChooseList(self):
        self._AddWordsToChooseList(self._data[Level.LevelNewWords])
        self._AddWordsToChooseList(self._data[Level.LevelInTraining])
        self._AddWordsToChooseList(self._data[Level.LevelLearned])
        self._AddWordsToChooseList(self._justTrained)
    
    def UpdateLevel(self, word, currentLevel, isWinLastGame, lastLenWinSeries):
        if isWinLastGame == False:
            self.RepeatWord(word)
        if currentLevel == Level.LevelNewWords and isWinLastGame:
            return Level.LevelInTraining
        if currentLevel == Level.LevelInTraining and lastLenWinSeries >= self._numOfWinToLevelUp:
            return Level.LevelLearned
        if currentLevel == Level.LevelLearned and isWinLastGame == False:
            return Level.LevelInTraining
        return currentLevel
    
    def _AddWordsToChooseList(self, data):
        data = sorted(data, key = lambda el: el.time)
        chunkData = []
        chunkList = []
        for dataWord in data:
            chunkList.append(dataWord.word)
            if len(chunkList) >= self._lenOfChunk:
                chunkData.append(chunkList)
                chunkList = []
        if chunkList:
            chunkData[len(chunkData) - 1].extend(chunkList) if chunkData else chunkData.append(chunkList)
        for chunk in chunkData:
            random.shuffle(chunk)
            self._wordsToChoose[:0] = chunk
    
    def _GetWordByIndex(self, index = -1):
        word = self._wordsToChoose.pop(index)
        self._wordsToChoose.insert(0, word)
        return word
    
    def _IsDelayNeeded(self, seriesOfWing, lastTrain):
        if seriesOfWing < 1:
            return False
        diff = time.time() - lastTrain
        if diff < seriesOfWing * self._delayAfterTrain:
            return True
        return False
