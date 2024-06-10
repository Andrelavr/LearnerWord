from Tools.Singleton import Singleton
from Tools.GoogleTranslator import GoogleTranslator
from Tools.Sound import Sound
from Core.AppSettings import AppSettings

class Pronunciation(metaclass=Singleton):
    def __init__(self) -> None:
        self._sounds = {}
        self._sortedNames = []
        self._maxNumOfSounds = 50
    
    def Load(self, word):
        if not word:
            return
        if word in self._sounds:
            if self._sortedNames[-1] != word:
                self._sortedNames.remove(word)
                self._sortedNames.append(word)
            return
        language = GoogleTranslator.languages.get(AppSettings().GetTranslateFromLang(), "en")
        self._sounds[word] = Sound(word, language)
        self._sortedNames.append(word)

    def Play(self, word):
        if not word:
            return
        self.Load(word)
        self._sounds[word].Play()
