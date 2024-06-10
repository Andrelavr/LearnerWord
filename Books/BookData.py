from Books.BookContent import BookContent
from Tools.BaseData import BaseData

class BookNames(BaseData):

    KeyAuthor = "author"
    KeyUrl = "url"

    def __init__(self) -> None:
        super().__init__()
        self._filename = "books"
    
    def GetNames(self) -> list:
        return list(self._data.keys())
    
    def GetAuthor(self, bookName) -> str:
        return self._GetValueByKey(bookName, BookNames.KeyAuthor, "")
    
    def GetUrl(self, bookName) -> str:
        return self._GetValueByKey(bookName, BookNames.KeyUrl, "")


class BookData(BaseData):

    KeyId = "id"
    KeyCurrentLine = "line"
    KeyNumberOfLines = "lines"

    def __init__(self) -> None:
        super().__init__()
        self._filename = "bookdata"
        self._nextId = 0
    
    def Init(self):
        super().Init()
        for book in self._data:
            self._nextId = max(self._nextId, int(self._GetValueByKey(book, BookData.KeyId, 0)))
        self._nextId = self._nextId + 1
    
    def GetId(self, bookName) -> str:
        id = self._GetValueByKey(bookName, BookData.KeyId, "")
        if not id:
            id = self._CreateNewId(bookName)
        return id
    
    def GetIds(self, bookList) -> dict:
        ids = {}
        for book in bookList:
            ids[self.GetId(book)] = book
        return ids

    def GetCurrentLine(self, bookName) -> int:
        return self._GetValueByKey(bookName, BookData.KeyCurrentLine, 0)
    
    def SetCurrentLine(self, bookName, line):
        self._SetValueByKey(bookName, BookData.KeyCurrentLine, line)
    
    def GetNumberOfBookLines(self, bookName) -> int:
        lines = self._GetValueByKey(bookName, BookData.KeyNumberOfLines, 0)
        if lines == 0:
            data = BookContent().GetBookContent(bookName)
            lines = len(data)
            self._SetValueByKey(bookName, BookData.KeyNumberOfLines, lines)
        return lines
    
    def _CreateNewId(self, bookName) -> str:
        id = str(self._nextId)
        self._nextId = self._nextId + 1
        self._SetValueByKey(bookName, BookData.KeyId, id)
        return id
