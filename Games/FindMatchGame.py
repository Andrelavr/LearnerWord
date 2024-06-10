from kivy.properties import ObjectProperty
from kivy.clock import Clock

from Games.BaseGame import BaseGame
from Games.GameButton import GameButtonState
from Dictionary.Dictionary import Dictionary
from Screens.UIElements import FindMatchPairButton

from enum import Enum
import time
import random

class MatchPairState(Enum):
    Correct = 1
    Failed = 2

class FindMatchPair:
    def __init__(self):
        self._left = None
        self._right = None
        self._resetTime = 0.5
    
    def SetLeft(self, btn):
        self._left = self._GetUpdatedPairValue(self._left, btn)
        return self._CheckPair()

    def SetRight(self, btn):
        self._right = self._GetUpdatedPairValue(self._right, btn)
        return self._CheckPair()

    def _GetUpdatedPairValue(self, oldValue, newValue):
        if self._left and self._right:
            return oldValue
        if oldValue:
            oldValue.SetState(GameButtonState.Default)
        newValue.SetState(GameButtonState.Active)
        return newValue
    
    def _CheckPair(self):
        if self._left == None or self._right == None:
            return None
        translations = Dictionary().GetUserMeanings(self._left.text)
        if self._right.text in translations:
            self._left.SetState(GameButtonState.Correct)
            self._right.SetState(GameButtonState.Correct)
            text = self._left.text
            self._left = self._right = None
            return (text, MatchPairState.Correct)
        else:
            self._left.SetState(GameButtonState.Wrong)
            self._right.SetState(GameButtonState.Wrong)
            Clock.schedule_once(self._ResetMistaken, self._resetTime)
            return (self._left.text, MatchPairState.Failed)
    
    def _ResetMistaken(self, dt):
        if self._left:
            self._left.SetState(GameButtonState.Default)
        if self._right:
            self._right.SetState(GameButtonState.Default)
        self._left = self._right = None


class FindMatchGame(BaseGame):
    gameLayout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._baseWords = []
        self._leftButtons = []
        self._rightButtons = []
        self._restartList = []
        self._matchPair = FindMatchPair()
        self._numOfWordsPerGame = 10
        self._timeRestartAnimation = 0.1
        self._correctAnswers = 0

    def on_kv_post(self, baseWidget):
        super().on_kv_post(baseWidget)
        self._BuildButtons()

    def StartNextGame(self):
        super().StartNextGame()
        self._correctAnswers = 0
        translations = []
        dictionary = Dictionary()
        for button in self._leftButtons:
            word = dictionary.GetNextWord()
            self.AddNexWord(word)
            translation = dictionary.GetUserMeanings(word)
            translations.append(random.choice(translation))
            self._baseWords.append(word)
            button.SetState(GameButtonState.Default)
            button.text = word
            button.bind(on_release = self.LeftButtonPress)
        random.shuffle(translations)
        for button in self._rightButtons:
            button.SetState(GameButtonState.Default)
            button.text = translations.pop()
            button.bind(on_release = self.RightButtonPress)
        self.GameStarted()
    
    def LeftButtonPress(self, btn):
        res = self._matchPair.SetLeft(btn)
        self._UpdateStateGame(res)

    def RightButtonPress(self, btn):
        res = self._matchPair.SetRight(btn)
        self._UpdateStateGame(res)

    def FinishGame(self):
        for word in self._baseWords:
            Dictionary().SetResultGame(word, self.IsWordFailed(word), time.time())
        self._baseWords = []
        self._restartList = self._leftButtons.copy()
        self._restartList.extend(self._rightButtons)
        random.shuffle(self._restartList)
        Clock.schedule_once(self._RestartAnimation, self._timeRestartAnimation)
    
    def _RestartAnimation(self, dt = 0.0):
        if self._restartList:
            button = self._restartList.pop()
            button.text = ""
            button.SetState(GameButtonState.Default)
            Clock.schedule_once(self._RestartAnimation, self._timeRestartAnimation)
        else:
            self.StartNextGame()
    
    def _UpdateStateGame(self, lastAnswer):
        if not lastAnswer:
            return
        if lastAnswer[1] == MatchPairState.Correct:
            self._correctAnswers += 1
        if lastAnswer[1] == MatchPairState.Failed:
            self.AddMistake(lastAnswer[0])
        if self._correctAnswers >= len(self._baseWords):
            self.FinishGame()

    def _BuildButtons(self):
        numWords = Dictionary().GetNumOfWords()
        if numWords < self._numOfWordsPerGame:
            self._numOfWordsPerGame = numWords
        for _ in range(self._numOfWordsPerGame):
            pairButton = FindMatchPairButton()
            self._leftButtons.append(pairButton.GetLeftButton())
            self._rightButtons.append(pairButton.GetRightButton())
            self.gameLayout.add_widget(pairButton)
