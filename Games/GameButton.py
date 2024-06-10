from kivy.properties import ObjectProperty

from Screens.FlatButton import FlatButton

from enum import Enum

class GameButtonState(Enum):
    Default = 0
    Correct = 1
    Wrong = 2
    Active = 3
    ActiveSelected = 4
    Invisible = 5

class GameButton(FlatButton):
    correctColor = ObjectProperty(None)
    wrongColor = ObjectProperty(None)
    activeColor = ObjectProperty(None)
    selectedActiveColor = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._state = GameButtonState.Default

    def SetState(self, state):
        if self._state == state:
            return
        self._state = state
        self._StateUpdated()
    
    def GetState(self):
        return self._state
    
    def _StateUpdated(self):
        pass
        match(self._state):
            case GameButtonState.Default:
                self._SetDefaultState()
            case GameButtonState.Correct:
                self._SetCorrectState()
            case GameButtonState.Wrong:
                self._SetWrongState()
            case GameButtonState.Active:
                self._SetActiveState()
            case GameButtonState.ActiveSelected:
                self._SetActiveSelectedState()
            case GameButtonState.Invisible:
                self._SetInvisible()

    def _SetWrongState(self):
        self.background_color = self.wrongColor
        self.set_disabled(True)

    def _SetCorrectState(self):
        self.background_color = self.correctColor
        self.set_disabled(True)
    
    def _SetDefaultState(self):
        self.background_color = self.defaultButtonColor
        self.usePressedState = True
        self.set_disabled(False)
    
    def _SetActiveState(self):
        self.background_color = self.activeColor
        self.usePressedState = False
    
    def _SetActiveSelectedState(self):
        self.background_color = self.selectedActiveColor
        self.usePressedState = False
    
    def _SetInvisible(self):
        self.background_color = (0.0, 0.0, 0.0, 0.0)
        self.text = ""
        self.set_disabled(True)

class GridItem(GameButton):
    gridMark = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.indexX = 0
        self.indexY = 0
        self.owners = []
    
    def SetMark(self, text):
        self.gridMark.text = text
    
    def GetMark(self):
        return self.gridMark.text
