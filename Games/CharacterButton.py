from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

class CharacterButton(BoxLayout):
    button = ObjectProperty(None)
    defaulColor = ObjectProperty(None)
    correctColor = ObjectProperty(None)
    wrongColor = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._owner = None
        self._activeButton = True
        self._waitToRemove = False

    def SetOwner(self, owner):
        self._owner = owner

    def SetText(self, text):
        self.button.text = text

    def ReleaseButton(self):
        if self._activeButton:
            self._activeButton = False
            if self._owner.CheckCharacter(self.button.text):
                self.SetCorrectStateWithTimer()
            else:
                self.SetWrongStateWithTimer()
    
    def ReactivateButton(self, dt = 0.0):
        if self._waitToRemove:
            return
        self.button.background_color = self.defaulColor
        if self._owner.CheckNeededCharacter(self.button.text):
            self._activeButton = True
        else:
            self._waitToRemove = True
            self.button.background_color = (0.0, 0.0, 0.0, 0.0)
            self.button.text = ''
    
    def SetWrongStateWithTimer(self):
        if self._waitToRemove:
            return
        self._activeButton = False
        self.button.background_color = self.wrongColor
        Clock.schedule_once(self.ReactivateButton, 0.2)

    def SetWrongState(self):
        if self._waitToRemove:
            return
        self.button.background_color = self.wrongColor

    def SetCorrectStateWithTimer(self):
        if self._waitToRemove:
            return
        self._activeButton = False
        self._activeButton = False
        self.button.background_color = self.correctColor
        Clock.schedule_once(self.ReactivateButton, 0.2)
    
    def SetCorrectState(self):
        if self._waitToRemove:
            return
        self.button.background_color = self.correctColor
