from Books.BookData import BookNames
from Books.BookData import BookData
from Books.BookContent import BookContent
from Books.WordsInBooks import WordsInBooks
from Tools.Singleton import Singleton

class Books(metaclass=Singleton):
    def __init__(self) -> None:
        self._bookNames = BookNames()
        self._bookData = BookData()
        self._bookContent = BookContent()
        self._bookNames.Init()
        self._bookData.Init()
        self._wordsInBooks = WordsInBooks(self._bookNames, self._bookData)
    
    def GetBooks(self):
        return self._bookNames.GetNames()
    
    def GetAuthor(self, book):
        return self._bookNames.GetAuthor(book)
    
    def GetCurrentLineOfBook(self, book):
        return self._bookData.GetCurrentLine(book)
    
    def SetCurrentLineOfBook(self, book, line):
        self._bookData.SetCurrentLine(book, line)
    
    def GetNumberOfBookLines(self, book):
        return self._bookData.GetNumberOfBookLines(book)
    
    def GetBookContent(self, bookName):
        return self._bookContent.GetBookContent(bookName)
    
    def Save(self):
        self._bookNames.Save()
        self._bookData.Save()
        self._wordsInBooks.Save()
    
    def StartSearchingWord(self, word, callback):
        self._wordsInBooks.StartSearchingWord(word, callback)

    def StopSearchingWord(self):
        self._wordsInBooks.StopSearching()

    def NumberOfWordOccurrences(self, word):
        return self._wordsInBooks.NumberOfOccurrences(word)

    def GetBooksWithWord(self, word):
        return self._wordsInBooks.GetBooks(word)

    def GetCurrentLineWithWord(self, word, book):
        return self._wordsInBooks.GetCurrentLineWithWord(word, book)

    def SetCurrentLineWithWord(self, word, book, line):
        self._wordsInBooks.SetCurrentLineWithWord(word, book, line)

    def GetNumberOfWordsInBook(self, word, book):
        return self._wordsInBooks.GetNumberOfWordsInBook(word, book)
