from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager

class MainScreen(ScreenManager):
    screenMgr = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._screenList = []
    
    def GoToScreen(self, newScreen, direction):
        self._screenList.append(self.screenMgr.current)
        self.screenMgr.current = newScreen
        self.screenMgr.transition.direction = direction
    
    def PopScreen(self):
        if self._screenList:
            screen = self._screenList.pop()
            self.screenMgr.current = screen
            self.screenMgr.transition.direction = "right"
    
    def GetScreenManager(self):
        return self.screenMgr
