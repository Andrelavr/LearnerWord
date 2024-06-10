import requests
from bs4 import BeautifulSoup

from Dictionary.WordsDataKeys import WordsDataKeys
from Dictionary.PrincetonData import PrincetonData
from Dictionary.BaseDataDownloader import BaseDataDownloader

class WordClass:
    Noun = "Noun"
    Verb = "Verb"
    Adjective = "Adjective"
    Adverb = "Adverb"

class PrincetonDictionary(BaseDataDownloader):
    def __init__(self) -> None:
        super().__init__()
        self._princetonUrl = "http://wordnetweb.princeton.edu/perl/webwn?s="
        self._wordClass = {
            '(n)' : WordClass.Noun,
            '(v)' : WordClass.Verb,
            '(adj)' : WordClass.Adjective,
            '(adv)' : WordClass.Adverb}
        self._refKeys = ['S:', 'W:']
        self._meanings = {}
        self._data = PrincetonData()
    
    def GetMeaning(self, word):
        meaning = self._data.GetPrincetonMeanings(word)
        return meaning

    def _Downloading(self):
        data = self._GetPrincetonData(self._text)
        self._ParseData(data)
        self._SaveData()
    
    def _GetPrincetonData(self, word):
        try:
            url = self._princetonUrl + word
            return requests.get(url).text
        except:
            return ""

    def _ParseData(self, html):
        try:
            html = BeautifulSoup(html, "html.parser")
            dataByWordClass = html.findChildren("ul")
            wordClassList = html.findAll("h3")
            for dataWord in dataByWordClass:
                wordClass = wordClassList[0].get_text() if wordClassList else ""
                dataMeanings = dataWord.findChildren("li")
                for dataMeaning in dataMeanings:
                    meaningTextList = [text for text in dataMeaning.stripped_strings]
                    usage = dataMeaning.find_next('i').get_text()
                    self._ParseMeanings(meaningTextList, usage, wordClass)
                if wordClassList:
                    wordClassList.pop(0)
        except:
            pass
    
    def _ParseMeanings(self, textList, usage, wordClass):
        if not textList:
            return
        if textList[0] in self._refKeys:
            textList.pop(0)
        currentWordClass = ""
        if textList[0] in self._wordClass:
            currentWordClass = self._wordClass[textList[0]]
            textList.pop(0)
        else:
            currentWordClass = wordClass
        updatedTextList = [text for text in textList if text != usage]
        meaning = " ".join(updatedTextList)
        meaning = meaning.replace(" ,", ",")
        self._AddMeaning(currentWordClass, meaning, usage)
    
    def _AddMeaning(self, wordClass, meaning, usage):
        if not meaning and not usage:
            return
        self._meanings.setdefault(wordClass, list())
        meaningObj = {}
        if meaning:
            meaningObj[WordsDataKeys.Meaning] = meaning
        if usage:
            meaningObj[WordsDataKeys.Usage] = usage
        self._meanings[wordClass].append(meaningObj)
    
    def _SaveData(self):
        self._data.AddPrincetonMeanings(self._text, self._meanings)
        self._meanings = {}
