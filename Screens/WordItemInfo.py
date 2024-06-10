from kivy.uix.bubble import Bubble

from Dictionary.Dictionary import Dictionary

class WordItemInfo(Bubble):
    
    def __init__(self, word, **kwargs):
        super().__init__(**kwargs)
        self.SetData(word)

    def SetData(self, word):
        dictionary = Dictionary()
        transcription = dictionary.GetTranscription(word)
        translation = dictionary.GetUserMeaningsStr(word)
        self.SetLabel("word", word)
        self.SetLabel("transcription", transcription)
        self.SetLabel("translation", translation)

    def SetLabel(self, name, value):
        label = self.ids.get(name, None)
        if label:
            label.text = value
