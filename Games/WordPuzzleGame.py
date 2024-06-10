from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from Games.BaseGame import BaseGame
from Games.CharacterButton import CharacterButton
from Dictionary.Dictionary import Dictionary
from Screens.FlatButton import FlatButton
from Screens.UIElements import UnicodeLabel
from Core.AppText import AppText

import random
import time

class WordPuzzleGame(BaseGame):
    translationText = ObjectProperty(None)
    baseWordText = ObjectProperty(None)
    bottomInfoLine1 = ObjectProperty(None)
    bottomInfoLine2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._buttonsPerLine = 10
        self._baseWord = ''
        self._puzzleWord = ''
        self._widgetLines = []
        self._buttonsDict = {}
        self._useKeyboard = True
        self._openDetailWhenFailed = True

    def on_kv_post(self, baseWidget):
        super().on_kv_post(baseWidget)
        self._widgetLines.append(self.ids["buttonsLine1"])
        self._widgetLines.append(self.ids["buttonsLine2"])
        self._widgetLines.append(self.ids["buttonsLine3"])

    def StartNextGame(self):
        super().StartNextGame()
        dictionary = Dictionary()
        self._baseWord = dictionary.GetNextWord()
        self.AddNexWord(self._baseWord)
        self.translationText.text = dictionary.GetUserMeaningsStr(self._baseWord)
        self.baseWordText.text = ''
        self._puzzleWord = ''
        self._SetInfoLines("Level: " + str(dictionary.GetWordLevel(self._baseWord)), '')
        self._ClearButtonWidgets()
        self._BuildCharButtons()
        self.LoadPronunciation(self._baseWord)
        self.GameStarted()

    def EnterPressed(self):
        if self.IsGameFinished():
            self.StartNextGame()

    def CharacterUp(self, char):
        if char in self._buttonsDict:
            self._buttonsDict[char].ReactivateButton()

    def CharacterDown(self, char):
        if self.CheckCharacter(char):
            self._buttonsDict[char].SetCorrectState()
        else:
            if char in self._buttonsDict:
                self._buttonsDict[char].SetWrongState()

    def CheckCharacter(self, ch):
        pos = len(self._puzzleWord)
        if pos < len(self._baseWord):
            if ch == self._baseWord[pos].lower():
                self._puzzleWord += ch
                self.baseWordText.text = self._puzzleWord
                self._SetInfoLines("Failed" if self.IsGameFailed() else "Correct", "")
                if self._puzzleWord == self._baseWord.lower():
                    self.FinishGame()
                return True
            else:
                self.AddMistake(self._baseWord)
                self._SetInfoLines('Failed', self._puzzleWord + ch)
        return False
    
    def CheckNeededCharacter(self, ch):
        if not ch:
            return
        pos = len(self._puzzleWord)
        return self._baseWord.lower().find(ch, pos) > -1

    def FinishGame(self):
        super().FinishGame()
        if not self.IsGameFailed():
            self.PlayPronunciation(self._baseWord)
        dictionary = Dictionary()
        self._ClearButtonWidgets()
        self.baseWordText.text = self._baseWord
        transcription = UnicodeLabel()
        transcription.text = dictionary.GetTranscription(self._baseWord)
        self._widgetLines[0].add_widget(transcription)
        nextButton = FlatButton()
        nextButton.text = AppText().GameNext
        nextButton.bind(on_release=self.NextGame)
        self._widgetLines[2].add_widget(nextButton)
        oldLevel = dictionary.GetWordLevel(self._baseWord)
        dictionary.SetResultGame(self._baseWord, self.IsGameFailed(), time.time())
        newLevel = dictionary.GetWordLevel(self._baseWord)
        allGames = dictionary.GetNumOfGames(self._baseWord)
        failGames = dictionary.GetNumOfWrongAns(self._baseWord)
        stateGame = "Fail!" if self.IsGameFailed() else "Correct."
        winSeries = dictionary.GetLastLenWinSeries(self._baseWord)
        info1 = stateGame + " Games: " + str(allGames) + ". Current Level: " + str(oldLevel) + ". Series of win: " + str(winSeries)
        info2 = "Correct answers: " + str(allGames - failGames) + ". Wrong: " + str(failGames) + ". New Level: " + str(newLevel)
        self._SetInfoLines(info1, info2)

    def NextGame(self, w = None):
        self.StartNextGame()

    def _ClearButtonWidgets(self):
        for line in self._widgetLines:
            elements = [el for el in line.children]
            for el in elements:
                line.remove_widget(el)

    def _BuildCharButtons(self):
        characters = set(el.lower() for el in self._baseWord)
        numCh = len(characters)
        charList = list(characters)
        random.shuffle(charList)
        createdButtons = 0
        self._AddPaddingForCharButtons(numCh)
        self._buttonsDict.clear()
        currentWidgetLine = 0
        for ch in charList:
            chButton = CharacterButton()
            chButton.SetText(ch)
            chButton.SetOwner(self)
            self._buttonsDict[ch] = chButton
            self._widgetLines[currentWidgetLine].add_widget(chButton)
            createdButtons += 1
            if createdButtons == self._buttonsPerLine:
                createdButtons = 0
                currentWidgetLine += 1

    def _AddPaddingForCharButtons(self, numOfChars):
        if numOfChars % self._buttonsPerLine != 0:
            paddingLayout = BoxLayout()
            paddingLayout.size_hint = ((self._buttonsPerLine - numOfChars % self._buttonsPerLine) * 0.05, 1.0)
            ind = int(numOfChars / self._buttonsPerLine)
            self._widgetLines[ind].add_widget(paddingLayout)

    def _SetInfoLines(self, line1, line2):
        self.bottomInfoLine1.text = line1
        self.bottomInfoLine2.text = line2
