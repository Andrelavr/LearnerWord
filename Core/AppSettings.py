from Tools.BaseData import BaseData
from Tools.Singleton import Singleton

class AppSettings(BaseData, metaclass=Singleton):

    KeyTranslateToLang = "translate_to"
    KeyTranslateFromLang = "translate_from"
    KeyAppLanguage = "app_language"
    KeyTranslatorActive = "translator_active"
    KeyPrincetonActive = "princeton_active"
    KeyAppTheme = "app_theme"

    def __init__(self) -> None:
        super().__init__()
        self._filename = "settings"
        self.Init()

    def GetTranslateToLang(self) -> str:
        return self._GetItem(AppSettings.KeyTranslateToLang, "english")
    
    def SetTranslateToLang(self, lang):
        self._SetItem(AppSettings.KeyTranslateToLang, lang)
        self.Save()
    
    def GetTranslateFromLang(self) -> str:
        return self._GetItem(AppSettings.KeyTranslateFromLang, "english")
    
    def SetTranslateFromLang(self, lang):
        self._SetItem(AppSettings.KeyTranslateFromLang, lang)
        self.Save()
    
    def GetAppLanguage(self) -> str:
        return self._GetItem(AppSettings.KeyAppLanguage, "english")
    
    def SetAppLanguage(self, lang):
        self._SetItem(AppSettings.KeyAppLanguage, lang)
        self.Save()
    
    def GetAppTheme(self) -> str:
        return self._GetItem(AppSettings.KeyAppTheme, "default")
    
    def SetAppTheme(self, theme):
        self._SetItem(AppSettings.KeyAppTheme, theme)
    
    def SetTranslatorActive(self, state):
        self._SetItem(AppSettings.KeyTranslatorActive, state)
    
    def GetTranslatorActive(self) -> bool:
        return self._GetItem(AppSettings.KeyTranslatorActive, True)
    
    def SetPrincetonActive(self, state):
        self._SetItem(AppSettings.KeyPrincetonActive, state)
    
    def GetPrincetonActive(self) -> bool:
        return self._GetItem(AppSettings.KeyPrincetonActive, True)
