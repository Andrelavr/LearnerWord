from Games.GameButton import GameButtonState

import random

class CrosswordItem:
    def __init__(self, word = "", items = [], startPos = -1) -> None:
        self._word = ""
        self._items = []
        self._selectedItem = None
        if word and items:
            self.AddWord(word, items, startPos)

    def GetItems(self):
        return self._items
    
    def GetWord(self):
        return self._word
    
    def GetSelectedItem(self):
        return self._selectedItem
    
    def IsHorizontal(self):
        if not self._items:
            return False
        ver = self._items[-1].indexX - self._items[0].indexX
        hor = self._items[-1].indexY - self._items[0].indexY
        if hor > ver:
            return True
        return False
    
    def CharInput(self, ch):
        if not self._selectedItem:
            return
        self._selectedItem.text = ch
        index = self._items.index(self._selectedItem)
        self._ChangeSelectedItem(index + 1)
    
    def BackInput(self):
        if not self._selectedItem:
            return
        self._selectedItem.text = ''
        index = self._items.index(self._selectedItem)
        self._ChangeSelectedItem(index - 1)
    
    def AddWord(self, word, items, startPos = -1):
        self._selectedItem = None
        self._word = word
        if startPos == -1:
            startPos = random.randint(0, len(items) - len(self._word))
        for ch, item in zip(self._word, items[startPos:]):
            item.SetState(GameButtonState.Default)
            item.text = ch
            item.owners.append(self)
            self._items.append(item)
    
    def AddFirstItemMark(self, mark):
        if not self._items:
            return
        if self._items[0].GetMark():
            isHor = self.IsHorizontal()
            marks = self._items[0].GetMark() if isHor else mark
            marks += "/" + (mark if isHor else self._items[0].GetMark())
            self._items[0].SetMark(marks)
        else:
            self._items[0].SetMark(mark)
    
    def CleanItems(self):
        for item in self._items:
            item.SetState(GameButtonState.Invisible)
            item.owners = []
            item.SetMark("")

    def SetInitialState(self):
        for item in self._items:
            item.SetState(GameButtonState.Default)
            item.text = ""
    
    def SetActiveState(self, state, selectedItem = None):
        for item in self._items:
            if state:
                if item == selectedItem:
                    item.SetState(GameButtonState.ActiveSelected)
                    self._selectedItem = item
                else:
                    item.SetState(GameButtonState.Active)
            else:
                item.SetState(GameButtonState.Default)
    
    def Check(self):
        if len(self._word) < len(self._items):
            return False
        corrects = 0
        for ind, item in enumerate(self._items):
            if item.GetState() == GameButtonState.Wrong:
                continue
            if item.text == self._word[ind].lower() or item.text == "" and self._word[ind] == ' ':
                item.SetState(GameButtonState.Correct)
                corrects += 1
            else:
                item.text = self._word[ind]
                item.SetState(GameButtonState.Wrong)
        if corrects == len(self._word):
            return True
        return False
    
    def _ChangeSelectedItem(self, nextIndex):
        if nextIndex < 0 or nextIndex >= len(self._items):
            return
        self._selectedItem.SetState(GameButtonState.Active)
        self._selectedItem = self._items[nextIndex]
        self._selectedItem.SetState(GameButtonState.ActiveSelected)
