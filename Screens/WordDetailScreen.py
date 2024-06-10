from kivy.properties import ObjectProperty
from kivy.app import App

from Screens.UIElements import CustomScreen
from Core.AppText import AppText
from Dictionary.Dictionary import Dictionary
from Tools.Pronunciation import Pronunciation
from Books.Books import Books

class WordDetail(CustomScreen):
    screenLayout = ObjectProperty(None)
    currentWordButton = ObjectProperty(None)
    meaningContent = ObjectProperty(None)
    wordNumber = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._words = []
        self._currentWordInd = 0

    def on_pre_enter(self, *args):
        super().on_pre_enter(self, *args)
        self._InitWordData()
    
    def on_enter(self, *args):
        super().on_enter(*args)
        Pronunciation().Play(self.GetCurrentWord())

    def on_leave(self, *args):
        super().on_leave(self, *args)
        Books().StopSearchingWord()
        self.meaningContent.ClearItems()
    
    def on_kv_post(self, baseWidget):
        super().on_kv_post(baseWidget)
        self.meaningContent.SetWordPressedCallback(self._OnWordPressed)
        self.meaningContent.SetTranslationCallback(self._OnTranslationPressed)
    
    def SetWord(self, word):
        if word not in self._words:
            self._words.append(word)
        self._currentWordInd = self._words.index(word)
    
    def PrevWord(self):
        if self._currentWordInd - 1 < 0:
            return
        self._currentWordInd -= 1
        self._UpdateWord()

    def NextWord(self):
        if self._currentWordInd + 1 >= len(self._words):
            return
        self._currentWordInd += 1
        self._UpdateWord()

    def GetCurrentWord(self):
        if self._currentWordInd < len(self._words):
            return self._words[self._currentWordInd]
        elif len(self._words) > 0:
            return self._words[-1]
        return ""
    
    def CurrentWordPressed(self):
        Pronunciation().Play(self.GetCurrentWord())
    
    def OpenBooks(self):
        App.get_running_app().GetScreenManager().get_screen("BookListScreen").BooksWithExamples(self.GetCurrentWord())
        App.get_running_app().GoToScreen("BookListScreen", "left")
    
    def _OnWordPressed(self, word):
        if word not in self._words:
            self._words.insert(self._currentWordInd + 1, word)
        self._currentWordInd = self._words.index(word)
        self._UpdateWord()
    
    def _UpdateWord(self):
        self._InitWordData()
        Pronunciation().Play(self.GetCurrentWord())
    
    def _UpdateWordNumberLabel(self):
        self.wordNumber.text = "{0}/{1}".format(self._currentWordInd + 1, len(self._words))
    
    def _OnTranslationPressed(self, translation):
        App.get_running_app().GetScreenManager().get_screen("AddWordScreen").SetWord(self.GetCurrentWord())
        App.get_running_app().GoToScreen("AddWordScreen", "left")
        App.get_running_app().GetScreenManager().get_screen("AddWordScreen").AddTranslation(translation)
    
    def _InitWordData(self):
        if not self.GetCurrentWord():
            return
        self.currentWordButton.text = self.GetCurrentWord()
        self.meaningContent.ClearItems()
        self._InitTranscriptionItem()
        self._InitMeaningItem()
        self.meaningContent.ShowMeaning(self.GetCurrentWord(), clearBeforeShow = False)
        if Dictionary().IsWordExist(self.GetCurrentWord()):
            Books().StartSearchingWord(self.GetCurrentWord(), self._InitExamplesButton)
        else:
            self._DisableExamplesButton()
        self._UpdateWordNumberLabel()

    def _InitTranscriptionItem(self):
        transcription = Dictionary().GetTranscription(self.GetCurrentWord())
        if transcription:
            self.meaningContent.AddCustomItem(transcription)

    def _InitMeaningItem(self):
        meaning = Dictionary().GetUserMeaningsStr(self.GetCurrentWord())
        if meaning:
            self.meaningContent.AddCustomItem(meaning)
    
    def _InitExamplesButton(self):
        examples = Books().NumberOfWordOccurrences(self.GetCurrentWord())
        if examples > 0: 
            self.screenLayout.headerButtonFunc = self.OpenBooks
            self.screenLayout.headerButtonText = AppText().WordExamples.format(examples)
        else:
            self._DisableExamplesButton()
    
    def _DisableExamplesButton(self):
        self.screenLayout.headerButtonFunc = False
