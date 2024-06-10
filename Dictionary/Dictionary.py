from Dictionary.WordOrderManager import WordOrderManager
from Dictionary.Level import Level
from Dictionary.WordsData import WordsData
from Dictionary.WordsData import GameData
from Dictionary.WordsReader import WordsReader
from Dictionary.PrincetonDictionary import PrincetonDictionary
from Dictionary.WordTranslator import WordTranslator
from Tools.Singleton import Singleton
from Tools.FunctionTime import FunctionTime

import random

class DownloadTaskData:
    TaskNamePrinceton = "princeton"
    TaskNameTranslator = "translator"
    def __init__(self, word = "", callback = None) -> None:
        self._word = word
        self._callback = callback
    
    def GetWord(self):
        return self._word
    
    def GetCallback(self):
        return self._callback

class Dictionary(metaclass=Singleton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._wordOrder = WordOrderManager()
        self._wordsData = WordsData()
        self._gameData = GameData()
        self._princeton = PrincetonDictionary()
        self._translator = WordTranslator()
        self._wordsList = []
        self._currentTask = {}
        self._InitDataBase()

    def GetUserMeanings(self, word):
        return self._wordsData.GetMeanings(word)
    
    def GetUserMeaningsStr(self, word):
        userMeanings = self.GetUserMeanings(word)
        return ", ".join(userMeanings)
    
    def GetTranscription(self, word):
        return self._wordsData.GetTranscription(word)
    
    def GetNumOfGames(self, word):
        return self._gameData.GetNumOfGames(word)
    
    def GetNumOfWrongAns(self, word):
        return self._gameData.GetNumOfWrongAns(word)
    
    def GetNumOfCorrectAns(self, word):
        return self.GetNumOfGames(word) - self.GetNumOfWrongAns(word)
    
    def GetLastLenWinSeries(self, word):
        return self._gameData.GetLastWinSeries(word)
    
    def GetWordLevel(self, word):
        return self._gameData.GetLevel(word)
    
    def GetTranslatorItems(self, word):
        return self._translator.GetTranslations(word)
    
    def AddOrEdit(self, word : str, transcription : str, meaning : list):
        self._wordsData.AddWord(word, transcription, meaning)
        self._wordOrder.RepeatWord(word)
        if word not in self._wordsList:
            self._wordsList.append(word)
        currentLevel = self.GetWordLevel(word)
        if currentLevel == Level.LevelIgnore or currentLevel == Level.LevelLearned:
            self._gameData.Update(word, level = Level.LevelInTraining)
    
    def DownloadTranslations(self, word, callback):
        if DownloadTaskData.TaskNameTranslator in self._currentTask:
            return
        self._currentTask[DownloadTaskData.TaskNameTranslator] = DownloadTaskData(word, callback)
        self._translator.Download(word, self._OnDownloadTranslations)
    
    def GetPrincetonMeanings(self, word):
        return self._princeton.GetMeaning(word)
    
    def DownloadPrincetonMeanings(self, word, callback):
        if DownloadTaskData.TaskNamePrinceton in self._currentTask:
            return
        self._currentTask[DownloadTaskData.TaskNamePrinceton] = DownloadTaskData(word, callback)
        self._princeton.Download(word, self._OnDownloadPrincetonMeanings)
    
    def SetWordLevel(self, word, level):
        if not Level.IsCorrectLevel(level):
            return
        if not self._wordsData.IsItemDataExist(word):
            return
        oldLevel = self.GetWordLevel(word)
        self._wordOrder.SetNewLevel(word, level)
        if oldLevel != level:
            self._gameData.Update(word, level = level)
    
    def GetNumOfWords(self):
        return len(self._wordsList)
    
    def GetNumOfWordsByLevel(self, level):
        num = 0
        for word in self._wordsList:
            if self.GetWordLevel(word) == level:
                num += 1
        return num
    
    def GetWordsByLevel(self, level):
        words = []
        for word in self._wordsList:
            if self.GetWordLevel(word) == level:
                words.append(word)
        return words
    
    def GetNextWord(self):
        return self._wordOrder.GetNextWord()
    
    def GetNextWordByFilter(self, filter):
        return self._wordOrder.GetNextWordByFilter(filter)
    
    def GetRandomUserMeaning(self):
        randWord = random.choice(self._wordsList)
        userMeanings = self.GetUserMeanings(randWord)
        if userMeanings:
            return random.choice(userMeanings)
        else:
            return "***"
    
    def GetRandomWord(self):
        return random.choice(self._wordsList)
    
    def UntrainedWord(self, word):
        if word:
            self._wordOrder.RepeatWord(word)
    
    def IsWordExist(self, word):
        return self._wordsData.IsItemDataExist(word)
    
    def RemoveWord(self, word):
        self._wordsData.RemoveItem(word)
        self._gameData.RemoveItem(word)
        self._wordOrder.RemoveWord(word)

    def SetResultGame(self, word, isFailed, time):
        if not self._wordsData.IsItemDataExist(word):
            return
        numOfGames = self._gameData.GetNumOfGames(word) + 1
        lastLenWinSeries = 0 if isFailed else self._gameData.GetLastWinSeries(word) + 1
        oldWrongAns = self._gameData.GetNumOfWrongAns(word)
        numOfWrongAns = oldWrongAns + 1 if isFailed else oldWrongAns
        oldLevel = self._gameData.GetLevel(word)
        newLevel = self._wordOrder.UpdateLevel(word, oldLevel, isFailed == False, lastLenWinSeries)
        self._gameData.Update(word, numOfGames, numOfWrongAns, lastLenWinSeries, time, newLevel)
    
    def Save(self):
        self._wordsData.Save()
        self._gameData.Save()
        self._princeton.Save()
        self._translator.Save()

    def _OnDownloadTranslations(self):
        if DownloadTaskData.TaskNameTranslator not in self._currentTask:
            return
        callback = self._currentTask[DownloadTaskData.TaskNameTranslator].GetCallback()
        if callback:
            callback()
        self._currentTask.pop(DownloadTaskData.TaskNameTranslator)

    def _OnDownloadPrincetonMeanings(self):
        if DownloadTaskData.TaskNamePrinceton not in self._currentTask:
            return
        callback = self._currentTask[DownloadTaskData.TaskNamePrinceton].GetCallback()
        if callback:
            callback()
        self._currentTask.pop(DownloadTaskData.TaskNamePrinceton)

    @FunctionTime
    def _InitDataBase(self):
        self._ReadDataBase()
        WordsReader(self._wordsData).Read()
        self._wordsList = list(self._wordsData.GetWordList())
        self._DistributeByLevels()

    @FunctionTime
    def _DistributeByLevels(self):
        for word in self._wordsList:
            self._wordOrder.SetWord(word, self.GetWordLevel(word), self.GetLastLenWinSeries(word), self._gameData.GetLastGameTime(word))
        self._wordOrder.InitChooseList()

    @FunctionTime
    def _ReadDataBase(self):
        self._wordsData.Init()
        self._gameData.Init()
        self._princeton.InitData()
        self._translator.InitData()
