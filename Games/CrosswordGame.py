from kivy.properties import ObjectProperty, ListProperty

from Games.BaseGame import BaseGame
from Games.CrosswordSystem import CrosswordSystem
from Dictionary.Dictionary import Dictionary
from Core.AppText import AppText

import time

class Crossword(BaseGame):
    mainField = ObjectProperty(None)
    crosswordAccordionItem = ObjectProperty(None)
    tipsScreenCheckButton = ObjectProperty(None)
    data = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._crosswordSystem = CrosswordSystem()
        self._useKeyboard = True
    
    def on_kv_post(self, baseWidget):
        super().on_kv_post(baseWidget)
        self._crosswordSystem.SetMainField(self.mainField)
        self._crosswordSystem.SetHintSetter(self.SetHeaderText)

    def CharacterDown(self, char):
        self._crosswordSystem.CharInput(char)
    
    def BackspacePressed(self):
        self._crosswordSystem.BackInput()
    
    def CheckPressed(self):
        if self.IsGameFinished():
            self.StartNextGame()
        else:
            self.CheckWords()
            self.crosswordAccordionItem.collapse = False
            self.FinishGame()
        self.ToggleButtons()
    
    def ToggleButtons(self):
        if self.IsGameFinished():
            self.screenLayout.headerButtonText = AppText().GameNext
            self.tipsScreenCheckButton.text = AppText().GameNext
        else:
            self.screenLayout.headerButtonText = AppText().CrosswordCheck
            self.tipsScreenCheckButton.text = AppText().CrosswordCheck

    def StartNextGame(self):
        super().StartNextGame()
        self._crosswordSystem.Generate()
        self.InitTips()
        self.GameStarted()
    
    def InitTips(self):
        self.data = []
        words = self._crosswordSystem.GetWords()
        for ind, word in enumerate(words):
            text = "{0}: {1}".format(ind + 1, Dictionary().GetUserMeaningsStr(word))
            self.data.append({"text":text, "word":word})
    
    def Select(self, word):
        self._crosswordSystem.SelectWord(word)
        self.crosswordAccordionItem.collapse = False
    
    def CheckWords(self):
        words = self._crosswordSystem.CheckWords()
        for word in words:
            Dictionary().SetResultGame(word, words[word], time.time())
