from kivy.properties import ObjectProperty
from kivy.app import App

from Books.Books import Books
from Screens.UIElements import CustomScreen

class BookListScreen(CustomScreen):

    recycleView = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self._booksWithExamples = []
        self._examplesForWord = ""
        self._examplesOpened = False
        self._sortByTitle = False
        self._sortByAuthor = False
        self._sortByState = True
    
    def on_pre_enter(self, *args):
        super().on_pre_enter(self, *args)
        self._PopulateData()
        self.recycleView.data = self.data
    
    def on_leave(self, *args):
        super().on_leave(*args)
        if self._examplesOpened == False:
            self._booksWithExamples = []
        self._examplesOpened = False
    
    def OpenBookReader(self, book):
        if self._booksWithExamples:
            App.get_running_app().GetScreenManager().get_screen("BookReaderScreen").ReadExamples(book, self._examplesForWord)
            self._examplesOpened = True
        else:
            App.get_running_app().GetScreenManager().get_screen("BookReaderScreen").ReadBook(book)
        App.get_running_app().GoToScreen("BookReaderScreen", "left")
    
    def BooksWithExamples(self, word):
        self._booksWithExamples = Books().GetBooksWithWord(word)
        self._examplesForWord = word
        
    def SortByTitle(self):
        self.recycleView.data = sorted(self.data, key = lambda el: el.get("title"), reverse = self._sortByTitle)
        self._sortByTitle = not self._sortByTitle

    def SortByAuthor(self):
        self.recycleView.data = sorted(self.data, key = lambda el: el.get("author"), reverse = self._sortByAuthor)
        self._sortByAuthor = not self._sortByAuthor

    def SortByReadingState(self):
        self.recycleView.data = sorted(self.data, key = lambda el: el.get("readState"), reverse = self._sortByState)
        self._sortByState = not self._sortByState

    def _PopulateData(self):
        books = Books()
        bookList = self._booksWithExamples if self._booksWithExamples else books.GetBooks()
        self.data.clear()
        for title in bookList:
            author = books.GetAuthor(title)
            state = ""
            if self._booksWithExamples:
                state = str(books.GetNumberOfWordsInBook(self._examplesForWord, title))
            else:
                currentLine = books.GetCurrentLineOfBook(title)
                if currentLine > 0:
                    state = "{0} %".format(round(currentLine / books.GetNumberOfBookLines(title) * 100))
            self.data.append({"title" : title, "author" : author, "readState" : state})
