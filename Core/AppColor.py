from kivy.properties import ListProperty
from kivy.event import EventDispatcher
from kivy.utils import get_color_from_hex

from Core.AppSettings import AppSettings
from Tools.BaseData import BaseData
from Tools.Singleton import Singleton

class AppColor(BaseData, EventDispatcher, metaclass=Singleton):

    Font = ListProperty()
    Background = ListProperty()
    FlatButton = ListProperty()
    FlatButtonPressed = ListProperty()
    ButtonCorrect = ListProperty()
    ButtonWrong = ListProperty()
    ButtonActive = ListProperty()
    ButtonSelectedActive = ListProperty()
    TextlineBackground = ListProperty()
    CrosswordBackground = ListProperty()
    CrosswordButtonActive = ListProperty()
    CrosswordButtonSelectedActive = ListProperty()
    CrosswordButtonCorrect = ListProperty()
    CrosswordButtonWrong = ListProperty()
    CrosswordFont = ListProperty()
    Transparent = ListProperty()
    TextInputBackground = ListProperty()
    TextInputForeground = ListProperty()
    TextInputHint = ListProperty()
    SwitchBackgroundOn = ListProperty()
    SwitchBackgroundOff = ListProperty()
    SwitchTextOn = ListProperty()
    SwitchTextOff = ListProperty()
    SwitchSlider = ListProperty()
    Separator = ListProperty()
    BookReaderBackground = ListProperty()
    BookFont = ListProperty()
    HeaderBackground = ListProperty()

    def __init__(self) -> None:
        super().__init__()
        self._filename = "appcolor"
        self._defaultcolor = "ffffff"
        self.Init()
        self.UpdateTheme()
    
    def GetThemes(self):
        return list(self._data.keys())
    
    def GetExampleTextColor(self):
        return self._Get("example_text")
    
    def GetSelectedTextColor(self):
        return self._Get("selected_text")
    
    def UpdateTheme(self):
        self._currentTheme = AppSettings().GetAppTheme()
        self.Font = self._GetColor("font")
        self.Background = self._GetColor("background")
        self.FlatButton = self._GetColor("flat_button")
        self.FlatButtonPressed = self._GetColor("flat_button_pressed")
        self.ButtonCorrect = self._GetColor("button_correct")
        self.ButtonWrong = self._GetColor("button_wrong")
        self.ButtonActive = self._GetColor("button_active")
        self.ButtonSelectedActive = self._GetColor("button_selected_active")
        self.TextlineBackground = self._GetColor("textline_background")
        self.CrosswordBackground = self._GetColor("crossword_background")
        self.CrosswordButtonActive = self._GetColor("crossword_button_active")
        self.CrosswordButtonSelectedActive = self._GetColor("crossword_button_selected_active")
        self.CrosswordButtonCorrect = self._GetColor("crossword_button_correct")
        self.CrosswordButtonWrong = self._GetColor("crossword_button_wrong")
        self.CrosswordFont = self._GetColor("crossword_font")
        self.Transparent = self._GetColor("transparent")
        self.TextInputBackground = self._GetColor("textinput_background")
        self.TextInputForeground = self._GetColor("textinput_foreground")
        self.TextInputHint = self._GetColor("textinput_hint")
        self.SwitchBackgroundOn = self._GetColor("switch_background_on")
        self.SwitchBackgroundOff = self._GetColor("switch_background_off")
        self.SwitchTextOn = self._GetColor("switch_text_on")
        self.SwitchTextOff = self._GetColor("switch_text_off")
        self.SwitchSlider = self._GetColor("switch_slider")
        self.Separator = self._GetColor("separator")
        self.BookReaderBackground = self._GetColor("book_reader_background")
        self.BookFont = self._GetColor("book_font")
        self.HeaderBackground = self._GetColor("header_background")

    def _GetColor(self, key) -> list:
        return get_color_from_hex(self._Get(key))

    def _Get(self, key) -> str:
        color = self._GetValueByKey(self._currentTheme, key, self._defaultcolor)
        if not color:
            color = self._GetValueByKey("default", key, self._defaultcolor)
        return color
