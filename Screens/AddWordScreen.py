from kivy.properties import ObjectProperty

from Screens.UIElements import CustomScreen
from Core.AppText import AppText
from Dictionary.Dictionary import Dictionary

import eng_to_ipa

class AddWordScreen(CustomScreen):
    inputWord = ObjectProperty(None)
    inputTranscription = ObjectProperty(None)
    inputTranslation = ObjectProperty(None)
    meaningContent = ObjectProperty(None)
    screenLayout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._word = ""
        self._userMeaning = []
        self._userMeaningText = ""
        self._transcriptionText = ""

    def on_pre_enter(self, *args):
        super().on_pre_enter(self, *args)
        self._UpdateWordData()
    
    def on_enter(self, *args):
        super().on_enter(*args)
        self.inputWord.focus = True

    def on_leave(self, *args):
        super().on_leave(self, *args)
        self.SetWord("")
        self.meaningContent.ClearItems()
    
    def on_kv_post(self, baseWidget):
        super().on_kv_post(baseWidget)
        self.meaningContent.SetWordPressedCallback(self._OnWordPressed)
        self.meaningContent.SetTranslationCallback(self._OnTranslationPressed)

    def SetWord(self, word):
        self._word = word.lower()
    
    def AddTranslation(self, translation):
        if not translation:
            return
        if translation in self._userMeaning:
            return
        self._userMeaning.append(translation)
        self._SetTranslationText()
        self._CheckIfDataChanged()
    
    def SaveButtonPressed(self):
        if not self._CheckInputs():
            return
        Dictionary().AddOrEdit(self._word, self.inputTranscription.text, self._userMeaning)
        self._DisableSaveButton()
    
    def TextUpdating(self):
        if self.inputWord.text == self._word:
            return
        self.SetWord(self.inputWord.text)
        self._UpdateTranslation([])
        if not self.inputWord.text:
            self.inputTranscription.text = ""
            self._DisableSaveButton()
            return
        if Dictionary().IsWordExist(self._word):
            self._UpdateDataFromDictionary()
        else:
            self._UpdateTranscription(self.inputWord.text)
            self._SetSaveButton()
    
    def TextUpdated(self):
        self.TextUpdating()
        if not self.inputWord.text:
            self.meaningContent.ClearItems()
            return
        if self.inputWord.focus == True:
            return
        self.meaningContent.ShowMeaning(self._word)
    
    def TranscriptionUpdated(self):
        if self._transcriptionText == self.inputTranscription.text:
            return
        self._transcriptionText = self.inputTranscription.text
        self._CheckIfDataChanged()
    
    def TranslationUpdated(self):
        if self._userMeaningText == self.inputTranslation.text:
            return
        self._userMeaningText = self.inputTranslation.text
        meaningList = [el.strip() for el in self._userMeaningText.split(',') if el.strip()]
        self._userMeaning = meaningList
        self._CheckIfDataChanged()
    
    def _DisableSaveButton(self):
        self.screenLayout.headerButtonFunc = False
    
    def _SetSaveButton(self):
        self.screenLayout.headerButtonFunc = self.SaveButtonPressed
        self.screenLayout.headerButtonText = AppText().WordSave
    
    def _SetEditButton(self):
        self.screenLayout.headerButtonFunc = self.SaveButtonPressed
        self.screenLayout.headerButtonText = AppText().WordEdit
    
    def _SetDefaultWordData(self):
        self.inputWord.text = ""
        self.inputTranscription.text = ""
        self.inputTranslation.text = ""
        self._userMeaning = []
        self._DisableSaveButton()
    
    def _OnTranslationPressed(self, translation):
        if translation in self._userMeaning:
            self._userMeaning.remove(translation)
        else:
            self._userMeaning.append(translation)
        self._SetTranslationText()
    
    def _SetTranslationText(self):
        if self._userMeaning:
            self.inputTranslation.text = ", ".join(self._userMeaning)
        else:
            self.inputTranslation.text = "".join(self._userMeaning)
    
    def _OnWordPressed(self, word):
        self.SetWord(word)
        self._UpdateWordData()
        
    def _UpdateWordData(self):
        if not self._word:
            self._SetDefaultWordData()
            return
        self.inputWord.text = self._word
        if Dictionary().IsWordExist(self._word):
            self._UpdateDataFromDictionary()
        else:
            self._UpdateTranscription(self._word)
            self._UpdateTranslation([])
            self._SetSaveButton()
        self.meaningContent.ShowMeaning(self._word)
    
    def _CheckIfDataChanged(self):
        if not Dictionary().IsWordExist(self._word):
            return
        transcription = Dictionary().GetTranscription(self._word) == self.inputTranscription.text
        meaning = Dictionary().GetUserMeanings(self._word) == self._userMeaning
        if meaning and transcription:
            self._DisableSaveButton()
            return
        self._SetEditButton()

    def _UpdateDataFromDictionary(self):
        self.inputTranscription.text = Dictionary().GetTranscription(self._word)
        self._UpdateTranslation(Dictionary().GetUserMeanings(self._word))
        self._DisableSaveButton()
    
    def _UpdateTranslation(self, meaning = []):
        self._userMeaning = meaning
        self._SetTranslationText()
    
    def _UpdateTranscription(self, text):
        transcription = eng_to_ipa.convert(text)
        self.inputTranscription.text = "[{0}]".format(transcription)
    
    def _CheckInputs(self):
        if not self.inputWord.text:
            self.inputWord.focus = True
            return False
        if not self.inputTranscription.text:
            self.inputTranscription.focus = True
            return False
        if not self.inputTranslation.text:
            self.inputTranslation.focus = True
            return False
        return True
