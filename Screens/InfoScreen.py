from kivy.properties import ObjectProperty

from Dictionary.Dictionary import Dictionary
from Dictionary.Level import Level
from Screens.UIElements import CustomScreen
from Screens.UIElements import InfoLine
from Core.AppText import AppText

class InfoScreen(CustomScreen):
    mainLayout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._widgetList = []

    def on_pre_enter(self, *args):
        super().on_pre_enter(self, *args)
        self._OpenInfo()

    def on_leave(self, *args):
        super().on_leave(self, *args)
        self._CloseInfo()
    
    def _OpenInfo(self):
        info = InfoLine()
        numOfWords = Dictionary().GetNumOfWords()
        info.SetText(AppText().WordsAllWords, str(numOfWords))
        self._AddWidget(info)
        levels = []
        levels.append([Level.LevelNewWords, AppText().WordsNew])
        levels.append([Level.LevelInTraining, AppText().WordsTraining])
        levels.append([Level.LevelLearned, AppText().WordsLearned])
        levels.append([Level.LevelIgnore, AppText().WordsIgnore])
        for level, levelStr in levels:
            wordsByLevel = Dictionary().GetNumOfWordsByLevel(level)
            info = InfoLine()
            info.SetText(levelStr, str(wordsByLevel))
            self._AddWidget(info)
    
    def _AddWidget(self, widget):
        self.mainLayout.add_widget(widget)
        self._widgetList.append(widget)

    def _CloseInfo(self):
        for widget in self._widgetList:
            self.mainLayout.remove_widget(widget)
        self._widgetList.clear()
