from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.bubble import Bubble

class UnicodeLabel(Label):
    pass

class CustomScreen(Screen):
    pass

class TrainingWordMenu(Bubble):
    pass

class LearnedWordMenu(Bubble):
    pass

class IgnoreWordMenu(Bubble):
    pass

class FindMatchPairButton(BoxLayout):

    def GetLeftButton(self):
        return self.ids["left"]
    
    def GetRightButton(self):
        return self.ids["right"]

class InfoLine(BoxLayout):
    leftLabel = ObjectProperty(None)
    rightLabel = ObjectProperty(None)

    def SetText(self, left, right):
        self.leftLabel.text = left
        self.rightLabel.text = right
