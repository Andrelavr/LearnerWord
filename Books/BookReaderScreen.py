from kivy.properties import ObjectProperty
from kivy.app import App

from Books.Books import Books
from Books.WordSearcher import WordSearcher
from Core.AppColor import AppColor
from Screens.UIElements import CustomScreen
from Tools.LabelTextConverter import LabelTextConverter

from math import ceil
from math import floor

class BookReaderScreen(CustomScreen):

    bookPage = ObjectProperty(None)
    pageLabel = ObjectProperty(None)
    leftPageButton = ObjectProperty(None)
    rightPageButton = ObjectProperty(None)
    screenLayout = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._bookData = []
        self._labels = []
        self._currentLine = 0
        self._bookName = ""
        self._examplesForWord = ""
        self._wordSearcher = None
        self._coloredTextTemplate = "[color={0}]{1}[/color]"
        self._exampleTextColor = "ffffff"
        self._labelConverters = {}
        self._selectedWords = []
    
    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self._labels = self.bookPage.children[::-1]
        for label in self._labels:
            self._labelConverters[label] = LabelTextConverter()
    
    def on_pre_enter(self, *args):
        super().on_pre_enter(self, *args)
        self._SetColors()
        self._InitReader()
    
    def on_pre_leave(self, *args):
        super().on_pre_leave(*args)
        if self._wordSearcher:
            self._wordSearcher.Clear()
        self._examplesForWord = ""
        self._selectedWords = []
        self._UpdateDetailButton()
    
    def DetailPressed(self):
        App.get_running_app().GetScreenManager().get_screen("WordDetail").SetWord(" ".join(self._selectedWords))
        App.get_running_app().GoToScreen("WordDetail", "left")

    def WordPressed(self, label, ref):
        index, word = self._labelConverters[label].ParseIndexedRef(ref)
        if self._labelConverters[label].IsWordColored(index):
            self._labelConverters[label].ToggleWordColorTag(index, False)
            self._selectedWords.remove(word)
        else:
            self._labelConverters[label].ToggleWordColorTag(index, True)
            self._selectedWords.append(word)
        self._UpdateDetailButton()
        label.text = self._labelConverters[label].GetConvertedText()
    
    def ReadExamples(self, book, word):
        self._bookName = book
        self._examplesForWord = word

    def ReadBook(self, book):
        self._bookName = book
    
    def LeftPage(self):
        if self._examplesForWord:
            self._currentLine = self._wordSearcher.FindPrevInBook(self._currentLine - 1)
            self._OpenPageWithExample()
            return
        if self._currentLine == 0:
            return
        self._currentLine = max(0, self._currentLine - len(self._labels))
        self._OpenPage(self._currentLine)
        Books().SetCurrentLineOfBook(self._bookName, self._currentLine)

    def RightPage(self):
        if self._examplesForWord:
            self._currentLine = self._wordSearcher.FindNextInBook(self._currentLine + 1)
            self._OpenPageWithExample()
            return
        if self._currentLine + len(self._labels) >= len(self._bookData):
            return
        self._currentLine = self._currentLine + len(self._labels)
        self._OpenPage(self._currentLine)
        Books().SetCurrentLineOfBook(self._bookName, self._currentLine)

    def _UpdateDetailButton(self):
        if self._selectedWords:
            self.screenLayout.headerButtonFunc = self.DetailPressed
        else:
            self.screenLayout.headerButtonFunc = False

    def _SetColors(self):
        self._exampleTextColor = AppColor().GetExampleTextColor()
        selectedText = AppColor().GetSelectedTextColor()
        for item in self._labelConverters.values():
            item.SetTextColor(selectedText)

    def _InitReader(self):
        if not self._bookName:
            return
        self._bookData = Books().GetBookContent(self._bookName)
        if self._examplesForWord:
            self._OpenBookWithExamples()
        else:
            self._OpenBook()
    
    def _OpenBook(self):
        self._currentLine = Books().GetCurrentLineOfBook(self._bookName)
        self.leftPageButton.disabled = False
        self.rightPageButton.disabled = False
        self._OpenPage(self._currentLine)
    
    def _OpenBookWithExamples(self):
        self._wordSearcher = WordSearcher()
        self._wordSearcher.Init(self._examplesForWord, self._bookName)
        self._currentLine = Books().GetCurrentLineWithWord(self._examplesForWord, self._bookName)
        if self._currentLine == 0:
            self._currentLine = self._wordSearcher.FindNextInBook()
        num = Books().GetNumberOfWordsInBook(self._examplesForWord, self._bookName)
        pageButtonDisabled = num == 1
        self.leftPageButton.disabled = pageButtonDisabled
        self.rightPageButton.disabled = pageButtonDisabled
        self._OpenPageWithExample()
    
    def _OpenPageWithExample(self):
        exampleLabel = int(len(self._labels) / 2)
        Books().SetCurrentLineWithWord(self._examplesForWord, self._bookName, self._currentLine)
        self._OpenPage(self._currentLine - exampleLabel)
        self._SelectExamples()
    
    def _SelectExamples(self):
        for label in self._labels:
            words = self._wordSearcher.FindInSting(label.text)
            for ind in words:
                coloredWord = self._coloredTextTemplate.format(self._exampleTextColor, words[ind])
                label.text = label.text[:ind] + label.text[ind:].replace(words[ind], coloredWord, 1)
    
    def _OpenPage(self, line):
        for ind, label in enumerate(self._labels):
            if line + ind < len(self._bookData) and line + ind >= 0:
                bookLine = self._bookData[line + ind]
                if self._examplesForWord:
                    label.text = bookLine
                else:
                    self._labelConverters[label].SetText(bookLine)
                    label.text = self._labelConverters[label].GetConvertedText()
            else:
                label.text = ""
        self._UpdatePageLabel()
    
    def _UpdatePageLabel(self):
        allPages = ceil(len(self._bookData) / len(self._labels))
        currentPage = floor(self._currentLine / len(self._labels)) + 1
        self.pageLabel.text = "{0}/{1}".format(currentPage, allPages)
