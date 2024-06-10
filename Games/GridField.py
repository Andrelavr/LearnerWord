from kivy.uix.boxlayout import BoxLayout

from Games.GameButton import GridItem
from Games.GameButton import GameButtonState

class GridField:
    
    def __init__(self, parent, callback):
        self._parent = parent
        self._callback = callback
        self._field = []
        self._minNumOfItems = 15
    
    def GenerateField(self):
        minSide = min(self._parent.width, self._parent.height)
        self.itemSize = int(minSide / self._minNumOfItems)
        numLines = int(self._parent.height / self.itemSize)
        self._parent.clear_widgets()
        self._field = []
        for line in range(numLines):
            self._CreateFieldLine(line)
    
    def GetField(self):
        if not self._field:
            self.GenerateField()
        return self._field

    def _CreateFieldLine(self, line):
        boxLine = BoxLayout()
        boxLine.orientation = "horizontal"
        boxLine.spacing = 1
        items = []
        numItems = int(self._parent.width / self.itemSize)
        for ind in range(numItems):
            item = self._CreateItem(line, ind)
            items.append(item)
            boxLine.add_widget(item)
        self._field.append(items)
        self._parent.add_widget(boxLine)

    def _CreateItem(self, indX, indY):
        item = GridItem()
        item.SetState(GameButtonState.Invisible)
        item.indexX = indX
        item.indexY = indY
        item.bind(on_release=self._callback)
        return item
