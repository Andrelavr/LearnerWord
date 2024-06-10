from Books.BookContent import BookContent
from Tools.AppLog import AppLog

class WordSearcher:

    consonants = ("b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z")
    vowels = ("a", "e", "i", "o", "u", "y")
    exceptionDoubling = ("x", "w")
    additionK = "ic"

    def __init__(self) -> None:
        self._InitValues()

    def Init(self, word, book):
        self._word = word.lower()
        self._bookName = book
        self._bookContent = BookContent().GetBookContent(self._bookName)
        self._endings = []
        self._changedChar = {}
        self._InitRootWord()
    
    def Clear(self):
        self._InitValues()
    
    def CountWordsInBook(self):
        count = 0
        for line in self._bookContent:
            count += self._CountWordsInLine(line)
        return count
    
    def FindInSting(self, string, startIndex = 0):
        lowerLine = string.lower()
        index = lowerLine.find(self._rootWord, startIndex)
        words = {}
        while(index != -1):
            word = self._IsSearchingWord(lowerLine, index)
            if word:
                words[index] = string[index : index + len(word)]
            index = lowerLine.find(self._rootWord, index + 1)
        return words
    
    def FindNextInBook(self, index = 0):
        for pos, line in enumerate(self._bookContent[index : ]):
            if self._CountWordsInLine(line) > 0:
                return index + pos
        for pos, line in enumerate(self._bookContent[ : index + 1]):
            if self._CountWordsInLine(line) > 0:
                return pos
        return -1

    def FindPrevInBook(self, index = 0):
        for pos, line in enumerate(self._bookContent[index : : -1]):
            if self._CountWordsInLine(line) > 0:
                return index - pos
        for pos, line in enumerate(self._bookContent[ : index - 1 : -1]):
            if self._CountWordsInLine(line) > 0:
                return len(self._bookContent) - pos - 1
        return -1
        
    def _InitValues(self):
        self._word = ""
        self._bookName = ""
        self._bookContent = []
        self._rootWord = ""
        self._endings = []
        self._changedVowels = []

    def _InitRootWord(self):
        self._rootWord = self._word
        if len(self._word) <= 2:
            return
        self._InitEndingsSeS()
        self._InitEndingsDeD()
        self._InitEndingsIng()
        
    def _IsChangedY(self):
        if self._word[-1] == 'y':
            if self._word[-2] in WordSearcher.consonants:
                return True
        return False
    
    def _IsDoublingConsonant(self):
        if self._word[-1] in WordSearcher.exceptionDoubling:
            return False
        if self._word[-1] in WordSearcher.consonants:
            if self._word[-2] in WordSearcher.vowels:
                return True
        return False
    
    def _IsAdditionK(self):
        if self._word.endswith(WordSearcher.additionK):
            return True
        return False
    
    def _InitEndingsSeS(self):
        if self._IsChangedY():
            self._AddChangedChar("y", "ies")
            self._ShortenRoot("y")
        self._endings.append("s")
        self._endings.append("es")
    
    def _InitEndingsDeD(self):
        if self._IsChangedY():
            self._AddChangedChar("y", "ied")
            self._ShortenRoot("y")
        elif self._IsAdditionK():
            self._endings.append("ked")
        elif self._IsDoublingConsonant():
            self._endings.append(self._word[-1] + "ed")
        elif self._word[-1] == "l":
            self._endings.append("led")
        self._endings.append("d")
        self._endings.append("ed")
    
    def _InitEndingsIng(self):
        if self._word.endswith("ie"):
            self._ShortenRoot("ie")
            self._AddChangedChar("i", "ying")
        if self._word[-1] == "e":
            self._ShortenRoot("e")
            self._AddChangedChar("e", "ing")
        elif self._IsAdditionK():
            self._endings.append("king")
        elif self._IsDoublingConsonant():
            self._endings.append(self._word[-1] + "ing")
        elif self._word[-1] == "l":
            self._endings.append("ling")
        self._endings.append("ing")

    def _AddChangedChar(self, ch, ending):
        self._changedChar.setdefault(ch, [])
        self._changedChar[ch].append(ending)
    
    def _ShortenRoot(self, ch):
        temp = self._word[ : -len(ch)]
        if len(temp) < len(self._rootWord):
            self._rootWord = temp
    
    def _CountWordsInLine(self, line):
        lowerLine = line.lower()
        index = lowerLine.find(self._rootWord)
        count = 0
        while(index != -1):
            if self._IsSearchingWord(lowerLine, index):
                count += 1
            index = lowerLine.find(self._rootWord, index + 1)
        return count
    
    def _HavePrefix(self, line, index):
        if index > 0:
            if line[index - 1].isalpha():
                return True
        return False

    def _IsSearchingWord(self, line, index):
        if self._HavePrefix(line, index):
            return ""
        ending = self._GetEnding(line, index + len(self._rootWord))
        if self._IsCorrectEnding(ending):
            return self._rootWord + ending
        return ""
    
    def _GetEnding(self, line, index):
        ending = ""
        for el in line[index:]:
            if not el.isalpha():
                return ending
            ending += el
        return ending
    
    def _IsCorrectEnding(self, ending):
        if not ending:
            if len(self._rootWord) == len(self._word):
                return True
            else:
                return False
        if self._rootWord + ending == self._word:
            return True
        correctCh = ""
        for ch in self._word[len(self._rootWord) : ]:
            if correctCh + ending in self._changedChar.get(ch, []):
                return True
            if ending.startswith(correctCh + ch):
                correctCh += ch
            else:
                return False
        if ending[len(correctCh) : ] in self._endings:
            return True
        return False
    
    def _Test(self):
        self._TestingData()
        for ind, word in enumerate(self._testContent):
            self._word = word
            self._bookContent = [self._testContent[word]]
            self._endings = []
            self._changedChar = {}
            self._InitRootWord()
            num = self.CountWordsInBook()
            AppLog().Log(AppLog.WordSearcher, "Testing. Search 2 words. Word {0}: {1} count: {2}".format(ind, word, num))

    def _TestingData(self):
        self._testContent = {
            "make":"make making",
            "take":"take taking",
            "forgive":"forgiving forgive",
            "write":"writing write",
            "agree":"agreeing agree",
            "fee":"fee feeing",
            "die":"die dying",
            "lie":"lying lie",
            "carry":"carrying carry",
            "study":"studying study",
            "worry":"worry worrying",
            "get":"getting get ",
            "occur":"occurring occur",
            "forget":"forgetting forget",
            "open":"opening open",
            "remember":"remembering remember",
            "cool":"cooling cool",
            "feel":"feeling feel",
            "mix":"mixing mix",
            "snow":"snowing snow",
            "signal":"signalling signal",
            "cancel":"canceling cancel ",
            "compel":"compelling compel ",
            "explore":"explored explore",
            "knee":"kneed knee",
            "marry":"married marry",
            "enjoy":"enjoyed enjoy",
            "permit":"permitted permit",
            "cool":"cool cooled",
            "annex":"annexed annex",
            "snow":"snow snowed",
            "travel":"travelled travel",
            "cancel":"canceled cancel",
            "compel":"compelled compel",
            "mimic":"mimicked mimic",
            "bus":"buses bus",
            "glass":"glasses glass",
            "box":"boxes box",
            "bench":"benches bench",
            "peach":"peach peaches",
            "crash":"crash crashes",
            "death":"deaths death",
            "touch":"touch touches",
            "buzz":"buzz buzzes",
            "smooth":"smooth smooths",
            "cherry":"cherries cherry",
            "butterfly":"butterflies butterfly",
            "monkey":"monkeys monkey",
            "essay":"essay essays",
            "imply":"implies imply",
            "play":"plays play",
            "radio":"radio radios",
            "buffalo":"buffalo buffaloes",
            "tomato":"tomatoes tomato",
            "solo":"soloes solo",
        }