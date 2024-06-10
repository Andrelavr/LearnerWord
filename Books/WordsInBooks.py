from Books.WordSearcher import WordSearcher
from Tools.BaseData import BaseData
from Tools.ThreadManager import ThreadManager
from Tools.AppLog import AppLog

class WordsInBooks(BaseData):
    KeyNumberOfWordsInBook = "num"
    KeyCurrentLineWithWord = "line"

    def __init__(self, books, booksData) -> None:
        super().__init__()
        self._filename = "wordsinbooks"
        self._compressEnabled = True
        self._books = books
        self._booksData = booksData
        self._searchingWord = ""
        self._preparedBookList = {}
        self._callback = None
        self._stopSearching = False
        self._wordSearcher = WordSearcher()
        self.Init()
    
    def NumberOfOccurrences(self, word):
        occurrencesList = self._data.get(word, {})
        number = 0
        for book in occurrencesList:
            number += occurrencesList[book].get(WordsInBooks.KeyNumberOfWordsInBook, 0)
        return number

    def GetBooks(self, word):
        ids = self._booksData.GetIds(self._books.GetNames())
        occurrencesList = self._data.get(word, {})
        books = []
        for id in occurrencesList:
            name = ids.get(id, "")
            num = occurrencesList[id].get(WordsInBooks.KeyNumberOfWordsInBook, 0)
            if name and num > 0:
                books.append(name)
        return books

    def GetCurrentLineWithWord(self, word, bookName):
        id = self._booksData.GetId(bookName)
        data = self._GetValueByKey(word, id, {})
        return data.get(WordsInBooks.KeyCurrentLineWithWord, 0)

    def SetCurrentLineWithWord(self, word, bookName, line):
        id = self._booksData.GetId(bookName)
        data = self._GetValueByKey(word, id, {})
        data[WordsInBooks.KeyCurrentLineWithWord] = line
        self._SetValueByKey(word, id, data)

    def GetNumberOfWordsInBook(self, word, bookName):
        id = self._booksData.GetId(bookName)
        data = self._GetValueByKey(word, id, {})
        return data.get(WordsInBooks.KeyNumberOfWordsInBook, 0)

    def StartSearchingWord(self, word, callback):
        AppLog().Log(AppLog.WordsInBooks, "StartSearchingWord. ID={0} word={1}".format(ThreadManager().GetThreadId(), word))
        self._searchingWord = word
        self._callback = callback
        self._stopSearching = False
        ThreadManager().RunNewThread("searchWords", self._PrepareBookList, self._OnPrepareBookList)
    
    def IsSearching(self):
        if self._searchingWord:
            return True
        return False
    
    def StopSearching(self):
        AppLog().Log(AppLog.WordsInBooks, "StopSearching. ID={0}".format(ThreadManager().GetThreadId()))
        self._stopSearching = True
    
    def _PrepareBookList(self):
        AppLog().Log(AppLog.WordsInBooks, "_PrepareBookList. ID={0}".format(ThreadManager().GetThreadId()))
        ids = self._booksData.GetIds(self._books.GetNames())
        booksInData = self._data.get(self._searchingWord, {})
        self._preparedBookList = {}
        for id in ids:
            if id in booksInData:
                continue
            else:
                self._preparedBookList[id] = ids[id]
    
    def _OnPrepareBookList(self):
        AppLog().Log(AppLog.WordsInBooks, "_OnPrepareBookList. ID={0} books={1}".format(ThreadManager().GetThreadId(), len(self._preparedBookList)))
        if self._stopSearching:
            self._FinishSearching()
            return
        if self._preparedBookList:
            ThreadManager().RunNewThread("searchWords", self._SearchInBook, self._OnPrepareBookList)
            if self._callback:
                self._callback()
        else:
            self._FinishSearching()

    def _SearchInBook(self):
        AppLog().Log(AppLog.WordsInBooks, "_SearchInBook. ID={0}".format(ThreadManager().GetThreadId()))
        id = ""
        bookName = ""
        for key in self._preparedBookList:
            id = key
            bookName = self._preparedBookList.pop(id)
            break
        self._wordSearcher.Init(self._searchingWord, bookName)
        numOfOccurrences = self._wordSearcher.CountWordsInBook()
        data = self._GetValueByKey(self._searchingWord, id, {})
        data[WordsInBooks.KeyNumberOfWordsInBook] = numOfOccurrences
        self._SetValueByKey(self._searchingWord, id, data)

    def _FinishSearching(self):
        AppLog().Log(AppLog.WordsInBooks, "_FinishSearching. ID={0}".format(ThreadManager().GetThreadId()))
        self._searchingWord = ""
        if not self._stopSearching and self._callback:
            self._callback()
        self._callback = None
        if self._wordSearcher:
            self._wordSearcher.Clear()
