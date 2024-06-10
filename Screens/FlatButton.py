from kivy.properties import ObjectProperty
from kivy.uix.button import Button

class FlatButton(Button):
    defaultButtonColor = ObjectProperty(None)
    pressedButtonColor = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._usePressedState = True

    def on_press(self):
        super().on_press()
        if self._usePressedState:
            self.background_color = self.pressedButtonColor

    def _do_release(self, *args):
        super()._do_release(args)
        if self._usePressedState:
            self.background_color = self.defaultButtonColor
