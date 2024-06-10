from Dictionary.TranslationItem import TranslationItem
from Tools.BaseData import BaseData
from Core.AppSettings import AppSettings

class TranslatorData(BaseData):
    def __init__(self) -> None:
        super().__init__()
        self._filename = "translatordata"
        self._compressEnabled = True

    def GetTranslatorItems(self, text):
        language = AppSettings().GetTranslateToLang()
        value = self._GetValueByKey(text.lower(), language, None)
        if not value:
            return []
        convertedItems = []
        for item in value:
            translationItem = TranslationItem()
            translationItem.FromObj(item)
            convertedItems.append(translationItem)
        return convertedItems
    
    def AddTranslatorItems(self, text, translationItems):
        translationList = []
        for item in translationItems:
            translationList.append(item.GetObj())
        language = AppSettings().GetTranslateToLang()
        self._SetValueByKey(text.lower(), language, translationList)
