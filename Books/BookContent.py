import os.path

class BookContent:
    def __init__(self) -> None:
        self._dataFolder = "Data"
        self._bookFolder = "Books"
        self._bookExt = ".txt"

    def GetBookContent(self, bookName):
        try:
            bookPath = os.path.join(self._dataFolder, self._bookFolder, bookName + self._bookExt)
            with open(bookPath, "r") as file:
                return file.readlines()
        except:
            return []
