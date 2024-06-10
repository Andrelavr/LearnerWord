from kivy.lang import Builder
from kivy.app import App
from kivy.clock import Clock

from Screens.MainScreen import MainScreen
from Books.Books import Books
from Dictionary.Dictionary import Dictionary
from Tools.ThreadManager import ThreadManager
from Core.AppSettings import AppSettings
from Core.AppText import AppText
from Core.AppColor import AppColor

import Screens.KivyScreens

from os import path

class MainApp(App):

    text = AppText()
    color = AppColor()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._updateInterval = 0.25
        self._dataFolder = "Data"
        self._SetTitle()

    def build(self):
        screensFolder = "Screens"
        mainScreen = "MainScreen.kv"
        Builder.load_file(path.join(self._dataFolder, screensFolder, mainScreen))
        self.mainScreen = MainScreen()
        return self.mainScreen
    
    def on_start(self):
        Clock.schedule_interval(self._Tick, self._updateInterval)
        return super().on_start()
    
    def GoToScreen(self, newScreen, direction):
        self.mainScreen.GoToScreen(newScreen, direction)

    def PopScreen(self):
        self.mainScreen.PopScreen()
    
    def GetScreenManager(self):
        return self.mainScreen.GetScreenManager()

    def Shutdown(self):
        Dictionary().Save()
        Books().Save()
        AppSettings().Save()
    
    def _SetTitle(self):
        logoFoler = "Logo"
        logoPic = "logo.png"
        self.icon = path.join(self._dataFolder, logoFoler, logoPic)
        self.title = "Learner Word"

    def _Tick(self, dt):
        ThreadManager().Update()
