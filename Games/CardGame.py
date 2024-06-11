from kivy.properties import ObjectProperty
from kivy.clock import Clock

from Games.BaseGame import BaseGame
from Games.GameButton import GameButtonState
from Dictionary.Dictionary import Dictionary

import random
import time

class CardGame(BaseGame):
    translationText = ObjectProperty(None)
    card1 = ObjectProperty(None)
    card2 = ObjectProperty(None)
    card3 = ObjectProperty(None)
    card4 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._cardWord = ""
        self._timeToNextGame = 1.6
        self._timeNewLetterAppear = 0.05
        self._openDetailWhenFailed = True

    def on_kv_post(self, baseWidget):
        super().on_kv_post(baseWidget)
        self._cards = []
        self._cards.append(self.card1)
        self._cards.append(self.card2)
        self._cards.append(self.card3)
        self._cards.append(self.card4)

    def StartNewGame(self):
        super().StartNewGame()
        self.StartNextGame()
        self.SetTitle()
        self.FillOutCards()

    def SetTitle(self):
        self.translationText.text = Dictionary().GetUserMeaningsStr(self._cardWord)

    def StartNextGame(self):
        super().StartNextGame()
        self._cardWord = Dictionary().GetNextWord()
        self.AddNexWord(self._cardWord)

    def FillOutCards(self):
        ansInd = random.randrange(0, len(self._cards))
        for ind, card in enumerate(self._cards):
            if ansInd == ind:
                card.text = self.GetTextForCorrectCard()
            else:
                card.text = self.GetTextForWrongCard()
        self.GameStarted()
    
    def GetTextForCorrectCard(self):
        text = self._cardWord
        return self.AddTranscription(text)

    def GetTextForWrongCard(self):
        text = Dictionary().GetRandomWord()
        return self.AddTranscription(text)
    
    def AddTranscription(self, word):
        transcription = Dictionary().GetTranscription(word)
        word += "\n"
        word += transcription
        return word

    def FinishGame(self):
        super().FinishGame()
        Dictionary().SetResultGame(self._cardWord, self.IsGameFailed(), time.time())
        for card in self._cards:
            if not self.IsCorrectCard(card):
                card.text = ""
        Clock.schedule_once(self.RestartGame, self._timeToNextGame)
    
    def IsCorrectCard(self, card):
        if card.text == "":
            return False
        return card.text.split('\n')[0] == self._cardWord

    def RestartGame(self, dt = 0.0):
        for card in self._cards:
            card.text = ""
            card.SetState(GameButtonState.Default)
        self.translationText.text = ""
        self.StartNextGame()
        Clock.schedule_once(self.WordAnimation, self._timeNewLetterAppear)
    
    def WordAnimation(self, dt = 0.0):
        translationText = Dictionary().GetUserMeaningsStr(self._cardWord)
        self.translationText.text = translationText[:len(self.translationText.text) + 1]
        if self.translationText.text == translationText:
            self.FillOutCards()
        else:
            Clock.schedule_once(self.WordAnimation, self._timeNewLetterAppear)
    
    def CheckCard(self, card):
        if self.IsGameFinished():
            return
        if card.text == "":
            return
        if self.IsCorrectCard(card):
            card.SetState(GameButtonState.Correct)
            self.FinishGame()
        else:
            card.SetState(GameButtonState.Wrong)
            self.AddMistake(self._cardWord)
