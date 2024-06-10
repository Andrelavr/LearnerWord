from kivy.properties import ObjectProperty

from Screens.UIElements import CustomScreen
from Core.AppSettings import AppSettings
from Core.AppText import AppText
from Core.AppColor import AppColor
from Tools.GoogleTranslator import GoogleTranslator

class SettingsScreen(CustomScreen):
    translateTo = ObjectProperty(None)
    translateFrom = ObjectProperty(None)
    appLanguage = ObjectProperty(None)
    appTheme = ObjectProperty(None)
    translatorSwitch = ObjectProperty(None)
    princetonSwitch = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_kv_post(self, baseWidget):
        super().on_kv_post(baseWidget)
        self._InitTranslateTo()
        self._InitTranslateFrom()
        self._InitAppLanguage()
        self._InitAppTheme()
        self._InitTranslatorSwitch()
        self._InitPrincetonSwitch()
        self._UpdateTexts()
    
    def TranslateToUpdated(self, updatedValue):
        currentSetting = AppSettings().GetTranslateToLang()
        if currentSetting != updatedValue:
            AppSettings().SetTranslateToLang(updatedValue)
    
    def TranslateFromUpdated(self, updatedValue):
        currentSetting = AppSettings().GetTranslateFromLang()
        if currentSetting != updatedValue:
            AppSettings().SetTranslateFromLang(updatedValue)
    
    def AppLanguageUpdated(self, updatedValue):
        currentLang = AppSettings().GetAppLanguage()
        if currentLang != updatedValue:
            AppSettings().SetAppLanguage(updatedValue)
            AppText().UpdateTexts()
            self._UpdateTexts()
    
    def AppThemeUpdated(self, updatedTheme):
        currentTheme = AppSettings().GetAppTheme()
        if currentTheme != updatedTheme:
            AppSettings().SetAppTheme(updatedTheme)
            AppColor().UpdateTheme()

    def TranslatorSwitchUpdated(self, updatedValue):
        if updatedValue != AppSettings().GetTranslatorActive():
            AppSettings().SetTranslatorActive(updatedValue)

    def PrincetonSwitchUpdated(self, updatedValue):
        if updatedValue != AppSettings().GetPrincetonActive():
            AppSettings().SetPrincetonActive(updatedValue)
    
    def _InitTranslateTo(self):
        self.translateTo.spinnerValues = GoogleTranslator.languages
        self.translateTo.settingSpinnerText = AppSettings().GetTranslateToLang()
        self.translateTo.settingChangedFunc = self.TranslateToUpdated
    
    def _InitTranslateFrom(self):
        self.translateFrom.settingDisabled = True
        self.translateFrom.spinnerValues = GoogleTranslator.languages
        self.translateFrom.settingSpinnerText = AppSettings().GetTranslateFromLang()
        self.translateFrom.settingChangedFunc = self.TranslateFromUpdated
    
    def _InitAppLanguage(self):
        self.appLanguage.spinnerValues = AppText().GetLanguages()
        self.appLanguage.settingSpinnerText = AppSettings().GetAppLanguage()
        self.appLanguage.settingChangedFunc = self.AppLanguageUpdated
    
    def _InitAppTheme(self):
        self.appTheme.spinnerValues = AppColor().GetThemes()
        self.appTheme.settingSpinnerText = AppSettings().GetAppTheme()
        self.appTheme.settingChangedFunc = self.AppThemeUpdated
    
    def _InitTranslatorSwitch(self):
        self.translatorSwitch.switchActive = AppSettings().GetTranslatorActive()
        self.translatorSwitch.settingChangedFunc = self.TranslatorSwitchUpdated

    def _InitPrincetonSwitch(self):
        self.princetonSwitch.switchActive = AppSettings().GetPrincetonActive()
        self.princetonSwitch.settingChangedFunc = self.PrincetonSwitchUpdated
    
    def _UpdateTexts(self):
        self.translateTo.settingLabel = AppText().SettingTranslateTo
        self.translateFrom.settingLabel = AppText().SettingTranslateFrom
        self.appLanguage.settingLabel = AppText().AppLanguage
        self.appTheme.settingLabel = AppText().AppTheme
        self.translatorSwitch.settingLabel = AppText().SettingTranslatorSwitch
        self.princetonSwitch.settingLabel = AppText().SettingPrincetonSwitch
