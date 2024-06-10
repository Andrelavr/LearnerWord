from Dictionary.TranslationItem import TranslationItem
from Dictionary.TranslatorData import TranslatorData
from Dictionary.BaseDataDownloader import BaseDataDownloader
from Tools.GoogleTranslator import GoogleTranslator
from Core.AppSettings import AppSettings

class WordTranslator(BaseDataDownloader):
    def __init__(self) -> None:
        super().__init__()
        self._translator = GoogleTranslator()
        self._translations = []
        self._data = TranslatorData()
    
    def GetTranslations(self, text) -> list:
        return self._data.GetTranslatorItems(text)
    
    def _IsTranslationExist(self, text) -> bool:
        return len(self._translations) > 0
    
    def _Downloading(self):
        try:
            fromLang = AppSettings().GetTranslateFromLang()
            toLang = AppSettings().GetTranslateToLang()
            data = self._translator.Translate(self._text, fromLang, toLang)
            self._ParseTranslatorData(data)
            self._SaveData()
        except:
            pass
        
    def _ParseTranslatorData(self, data):
        if not self._CheckListData(data):
            return
        wordIndexData = 3
        phraseIndexData = 1
        if self._CheckListIndex(data, wordIndexData):
            self._ParseWordTranslatorData(data[wordIndexData])
        elif self._CheckListIndex(data, phraseIndexData):
            self._ParsePhraseTranslatorData(data[phraseIndexData])

    def _ParseWordTranslatorData(self, data):
        innerTranslatorDataIndex = 5
        translationsListObjectIndex = 0
        translationsIndex = 1
        innerTranslatorData = self._GetDataFromList(data, innerTranslatorDataIndex)
        translationsListObject = self._GetDataFromList(innerTranslatorData, translationsListObjectIndex)
        if not self._CheckListData(translationsListObject):
            return
        for translationItem in translationsListObject:
            translations = self._GetDataFromList(translationItem, translationsIndex)
            self._AddWordTranslations(translations)
    
    def _AddWordTranslations(self, translations):
        if not self._CheckListData(translations):
            return
        translationIndex = 0
        synonymsIndex = 2
        frequencyIndex = 3
        for translationItem in translations:
            translation = self._GetDataFromList(translationItem, translationIndex)
            synonyms = self._GetDataFromList(translationItem, synonymsIndex, [])
            frequency = self._GetDataFromList(translationItem, frequencyIndex, 0)
            if translation:
                self._AddTranslationItem(TranslationItem(translation, synonyms, frequency))

    def _ParsePhraseTranslatorData(self, data):
        phraseTranslationDataIndex = 0
        phraseTranslationInnerDataIndex = 0
        phraseTranslationsIndex = 5
        phraseMainTranslationIndex = 0
        phraseTranslationData = self._GetDataFromList(data, phraseTranslationDataIndex)
        phraseTranslationInnerData = self._GetDataFromList(phraseTranslationData, phraseTranslationInnerDataIndex)
        phraseTranslations = self._GetDataFromList(phraseTranslationInnerData, phraseTranslationsIndex)
        phraseMainTranslation = self._GetDataFromList(phraseTranslations, phraseMainTranslationIndex)
        self._AddPhraseTranslations(phraseMainTranslation)

    def _AddPhraseTranslations(self, data):
        translationTextIndex = 0
        additionalTranslationsIndex = 4
        mainTranslationText = self._GetDataFromList(data, translationTextIndex, "")
        additionalTranslations = self._GetDataFromList(data, additionalTranslationsIndex, [])
        for additional in additionalTranslations:
            additionalTranslationText = self._GetDataFromList(additional, translationTextIndex, "")
            if additionalTranslationText:
                self._AddTranslationItem(TranslationItem(translation = additionalTranslationText))
        if not self._IsTranslationExist(self._text):
            self._AddTranslationItem(TranslationItem(translation = mainTranslationText))

    def _AddTranslationItem(self, item):
        self._translations.append(item)

    def _CheckListData(self, data):
        if isinstance(data, list):
            return True
        return False
        
    def _CheckListIndex(self, data, index):
        if index >= 0 and index < len(data):
            return True
        return False
    
    def _GetDataFromList(self, data, index, default = None):
        if self._CheckListData(data) and self._CheckListIndex(data, index):
            return data[index]
        return default
    
    def _SaveData(self):
        if not self._translations:
            return
        self._data.AddTranslatorItems(self._text, self._translations)
        self._translations = []
