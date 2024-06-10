from kivy.clock import Clock

from Games.CardGame import CardGame
from Dictionary.Dictionary import Dictionary

import random

class TranslationCardGame(CardGame):

    def SetTitle(self):
        text = self._cardWord
        transcription = Dictionary().GetTranscription(self._cardWord)
        text += "\n"
        text += transcription
        self.translationText.text = text

    def GetTextForCorrectCard(self):
        return random.choice(Dictionary().GetUserMeanings(self._cardWord))

    def GetTextForWrongCard(self):
        return Dictionary().GetRandomUserMeaning()

    def IsCorrectCard(self, card):
        translation = Dictionary().GetUserMeanings(self._cardWord)
        if card.text in translation:
            return True
        return False

    def WordAnimation(self, dt = 0.0):
        animatedText = self.translationText.text.split('\n')
        animatedText = self._cardWord[:len(animatedText[0]) + 1]
        self.translationText.text = animatedText + "\n[]"
        if animatedText == self._cardWord:
            self.translationText.text = self.AddTranscription(animatedText)
            self.FillOutCards()
        else:
            Clock.schedule_once(self.WordAnimation, self._timeNewLetterAppear)
