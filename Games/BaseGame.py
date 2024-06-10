from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.core.window import Window
from kivy.core.window import Keyboard

from Screens.UIElements import CustomScreen
from Core.AppText import AppText
from Tools.Pronunciation import Pronunciation
from Dictionary.Dictionary import Dictionary

from enum import Enum

class GameState(Enum):
    Default = 0
    GameStarted = 1
    GameFinished = 2
    GameRestarting = 3

class BaseGame(CustomScreen):
    screenLayout = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self._gamesCounter = 0
        self._failGamesCounter = 0
        self._gameState = GameState.Default
        self._gameFailed = False
        self._wordsMistakes = {}
        self._useKeyboard = False
        self._keyboard = None
        self._openDetailWhenFailed = False
        self._keycodeEnter = Keyboard.keycodes["enter"]
        self._keycodeBackspace = Keyboard.keycodes["backspace"]
        self._keycodeSpacebar = Keyboard.keycodes["spacebar"]
        self._keycodeA = Keyboard.keycodes["a"]
        self._keycodeZ = Keyboard.keycodes["z"]
    
    def on_pre_enter(self, *args):
        super().on_pre_enter(self, *args)
        self.StartNewGame()

    def on_leave(self, *args):
        super().on_leave(self, *args)
        self.CloseGame()
    
    def CloseGame(self):
        self.CloseKeyboard()
        dictionary = Dictionary()
        dictionary.Save()
        if not self.IsGameStarted():
            return
        for word in self._wordsMistakes:
            Dictionary().UntrainedWord(word)
    
    def DetailPressed(self):
        for word in self._wordsMistakes:
            App.get_running_app().GetScreenManager().get_screen("WordDetail").SetWord(word)
            App.get_running_app().GoToScreen("WordDetail", "left")
            return
    
    def SetGameState(self, state):
        self._gameState = state
    
    def IsGameStarted(self):
        return self._gameState == GameState.GameStarted
    
    def IsGameFinished(self):
        return self._gameState == GameState.GameFinished
    
    def IsGameFailed(self):
        return self._gameFailed

    def FinishGame(self):
        self.SetGameState(GameState.GameFinished)
        if self.IsGameFailed():
            self._failGamesCounter += 1
        self.UpdateHeaderLabel()
        if self._openDetailWhenFailed and self.IsGameFailed():
            self.DetailPressed()

    def UpdateHeaderLabel(self):
        self.SetHeaderText(AppText().GameHeader.format(self._gamesCounter, self._failGamesCounter))
    
    def SetHeaderText(self, text):
        self.screenLayout.headerLabelText = text
    
    def StartNewGame(self):
        self.OpenKeyboard()
        self.StartNextGame()

    def StartNextGame(self):
        self._gamesCounter += 1
        self._gameFailed = False
        self._wordsMistakes = {}
    
    def GameStarted(self):
        self.SetGameState(GameState.GameStarted)
    
    def AddNexWord(self, word):
        self._wordsMistakes[word] = False
    
    def AddMistake(self, word):
        self._gameFailed = True
        self._wordsMistakes[word] = True
    
    def IsWordFailed(self, word):
        return self._wordsMistakes.get(word, False)
    
    def LoadPronunciation(self, word):
        Pronunciation().Load(word)
    
    def PlayPronunciation(self, word):
        Pronunciation().Play(word)
    
    def OpenKeyboard(self):
        if not self._useKeyboard:
            return
        self._keyboard = Window.request_keyboard(self.CloseKeyboard, self)
        self._keyboard.bind(on_key_up=self.KeyUp)
        self._keyboard.bind(on_key_down=self.KeyDown)

    def CloseKeyboard(self):
        if not self._useKeyboard:
            return
        if not self._keyboard:
            return
        self._keyboard.unbind(on_key_up=self.KeyUp)
        self._keyboard.unbind(on_key_down=self.KeyDown)
        self._keyboard = None
        Window.release_keyboard(self)
    
    def KeyUp(self, keyboard, keycode):
        if not isinstance(keycode, tuple):
            return
        ch = self.GetCharByKeycode(keycode)
        if ch:
            self.CharacterUp(ch)
        elif keycode[0] == self._keycodeEnter:
            self.EnterPressed()
        elif keycode[0] == self._keycodeBackspace:
            self.BackspacePressed()
    
    def KeyDown(self, keyboard, keycode, text, modifiers):
        if not isinstance(keycode, tuple):
            return
        ch = self.GetCharByKeycode(keycode)
        if ch:
            self.CharacterDown(ch)
    
    def GetCharByKeycode(self, keycode):
        if keycode[0] >= self._keycodeA and keycode[0] <= self._keycodeZ or keycode[0] == self._keycodeSpacebar:
            char = ' ' if keycode[0] == self._keycodeSpacebar else keycode[1]
            return char
        return ''
    
    def BackspacePressed(self):
        pass

    def EnterPressed(self):
        pass

    def CharacterUp(self, char):
        pass

    def CharacterDown(self, char):
        pass
