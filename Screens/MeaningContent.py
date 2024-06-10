from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

from Core.AppSettings import AppSettings
from Dictionary.Dictionary import Dictionary
from Dictionary.WordsDataKeys import WordsDataKeys
from Tools.LabelTextConverter import LabelTextConverter

class MeaningWordItem(BoxLayout):
    pass

class MeaningWordMarkItem(MeaningWordItem):
    pass

class MeaningContent(ScrollView):
    scrollContent = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._textConverter = LabelTextConverter()
        self._word = ""
        self._indentDefault = 0
        self._indentMain = 1
        self._indentAddition = 2
        self._frequencyMark = [ '', '\u25C6', '\u25C8', '\u25C7']
        self._wordPressedCallback = None
        self._translationCallback = None
    
    def SetWordPressedCallback(self, callback):
        self._wordPressedCallback = callback
    
    def SetTranslationCallback(self, callback):
        self._translationCallback = callback
    
    def AddCustomItem(self, text):
        self._InitItem(text, self._indentMain)
    
    def ShowMeaning(self, word, princetonMeaning = True, translation = True, clearBeforeShow = True):
        self._word = word
        if clearBeforeShow:
            self.ClearItems()
        princetonEnabled = AppSettings().GetPrincetonActive()
        if princetonMeaning and princetonEnabled:
            self._InitPrincetonMeanings()
        translatorEnabled = AppSettings().GetTranslatorActive()
        if translation and translatorEnabled:
            self._InitTranslations()

    def ClearItems(self):
        self.scrollContent.clear_widgets()
        _, paddingTop, _, paddingBottom = self.scrollContent.padding
        self.scrollContent.height = paddingTop + paddingBottom
    
    def _OnWordPressed(self, widget, word):
        if self._wordPressedCallback:
            self._wordPressedCallback(word)
    
    def _OnTranslationPressed(self, widget, word):
        if self._translationCallback:
            self._translationCallback(word)
    
    def _InitTranslations(self):
        translations = Dictionary().GetTranslatorItems(self._word)
        if not translations:
            Dictionary().DownloadTranslations(self._word, self._DownloadTranslationsFinished)
            return
        self._InitTranslationList(translations)
    
    def _DownloadTranslationsFinished(self):
        translations = Dictionary().GetTranslatorItems(self._word)
        self._InitTranslationList(translations)
    
    def _InitTranslationList(self, translations):
        for translationItem in translations:
            self._InitTranslationItem(translationItem.GetTranslation(), translationItem.GetFrequency())
            self._InitSynonymsItem(translationItem.GetSynonyms())
    
    def _InitTranslationItem(self, translation, frequence):
        self._InitMarkItem(self._textConverter.MakeRef(translation), self._indentMain, frequence)
    
    def _InitSynonymsItem(self, synonyms):
        if synonyms:
            refList = self._textConverter.MakeRefsFromList(synonyms)
            self._InitItem(", ".join(refList), self._indentAddition)
    
    def _InitPrincetonMeanings(self):
        princetonMeanings = Dictionary().GetPrincetonMeanings(self._word)
        if not princetonMeanings:
            Dictionary().DownloadPrincetonMeanings(self._word, self._DownloadPrincetonMeaningsFinished)
            return
        self._InitPrincetonMeaningList(princetonMeanings)
    
    def _DownloadPrincetonMeaningsFinished(self):
        princetonMeanings = Dictionary().GetPrincetonMeanings(self._word)
        self._InitPrincetonMeaningList(princetonMeanings)
    
    def _InitPrincetonMeaningList(self, meanings):
        for wordClass in meanings:
            self._InitWordClassItem(wordClass)
            self._InitMeaningList(meanings[wordClass])
    
    def _InitWordClassItem(self, wordClass):
        self._InitItem(wordClass)
    
    def _InitMeaningList(self, meaningList):
        for meaningItem in meaningList:
            if WordsDataKeys.Meaning in meaningItem:
                self._InitPrincetonMeaningItem(meaningItem[WordsDataKeys.Meaning])
            if WordsDataKeys.Usage in meaningItem:
                self._InitPrincetonUsageItem(meaningItem[WordsDataKeys.Usage])
    
    def _InitPrincetonMeaningItem(self, meaning):
        self._InitItemWithRefs(meaning, self._indentMain)
    
    def _InitPrincetonUsageItem(self, usage):
        self._InitItemWithRefs(usage, self._indentAddition)
    
    def _InitItemWithRefs(self, text, indent):
        self._InitItem(self._textConverter.MakeRefs(text), indent)

    def _InitItem(self, text, indent = 0):
        item = MeaningWordItem()
        item.itemLabel.bind(on_ref_press=self._OnWordPressed)
        self._SetupAndAddWidget(item, text, indent)
    
    def _InitMarkItem(self, text, indent = 1, frequency = 0):
        item = MeaningWordMarkItem()
        item.markLabel.text = self._frequencyMark[frequency] if frequency >= 0 and frequency < len(self._frequencyMark) else ''
        item.itemLabel.bind(on_ref_press=self._OnTranslationPressed)
        self._SetupAndAddWidget(item, text, indent)
    
    def _SetupAndAddWidget(self, widget, text, indent):
        widget.itemLabel.text = text
        self._SetIndent(widget, indent)
        widget.bind(height=self._HeightUpdated)
        self.scrollContent.add_widget(widget)
    
    def _SetIndent(self, widget, indent = 0):
        if not widget:
            return
        if indent == self._indentDefault:
            widget.itemLabel.padding = widget.indentDefault
        elif indent == self._indentMain:
            widget.itemLabel.padding = widget.indentMain
        elif indent == self._indentAddition:
            widget.itemLabel.padding = widget.indentAddition
        else:
            widget.itemLabel.padding = widget.indentDefault
    
    def _HeightUpdated(self, widget, height):
        if abs(widget.prevHeight - widget.height) < 0.1:
            return
        self.scrollContent.height -= widget.prevHeight
        self.scrollContent.height += height
        widget.prevHeight = height
