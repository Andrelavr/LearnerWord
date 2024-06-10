class TranslationItem:
    KeyTranslation = "tr"
    KeySynonyms = "synonym"
    KeyFrequence = "frequence"

    def __init__(self, translation = "", synonyms = [], frequence = 0) -> None:
        self._data = {}
        self._data[TranslationItem.KeyTranslation] = translation
        self._data[TranslationItem.KeySynonyms] = synonyms
        self._data[TranslationItem.KeyFrequence] = frequence
    
    def GetTranslation(self) -> str:
        return self._data.get(TranslationItem.KeyTranslation, "")
    
    def GetSynonyms(self) -> list:
        return self._data.get(TranslationItem.KeySynonyms, [])
    
    def GetFrequency(self) -> int:
        return self._data.get(TranslationItem.KeyFrequence, 0)
    
    def GetObj(self):
        return self._data
    
    def FromObj(self, obj):
        self._data = obj
