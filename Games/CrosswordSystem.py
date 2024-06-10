from Games.GridField import GridField
from Games.CrosswordItem import CrosswordItem
from Dictionary.Dictionary import Dictionary
from Dictionary.WordFilter import WordFilter
from Tools.FunctionTime import FunctionTime
from Tools.AppLog import AppLog

import random

class CrosswordSystem:
    def __init__(self) -> None:
        self._field = []
        self._maxNumOfWords = 100
        self._crosswordItems = []
        self._generating = []
        self._selectedItem = None
        self._mainField = None
        self._hintSetter = None
        self._InitFilter()
    
    def SetMainField(self, mainField):
        self._mainField = mainField
    
    def SetHintSetter(self, setter):
        self._hintSetter = setter
    
    def GetWords(self):
        return [el.GetWord() for el in self._crosswordItems]

    def CrosswordButtonPressed(self, button):
        if button.owners:
            self.SelectItem(button)
    
    def SelectWord(self, word):
        self._DeselectItem()
        for item in self._crosswordItems:
            if item.GetWord() == word:
                item.SetActiveState(True, item.GetItems()[0])
                self.SetSelectedItem(item)
    
    def SetSelectedItem(self, item):
        self._selectedItem = item
        self._ShowHint()
    
    def SelectItem(self, button):
        self._DeselectItem()
        if self._selectedItem and button == self._selectedItem.GetSelectedItem():
            if self.SelectCrossItem(button):
                return
        self.SetSelectedItem(self._selectedItem if self._selectedItem in button.owners else button.owners[0])
        self._selectedItem.SetActiveState(True, button)
    
    def CharInput(self, ch):
        if self._selectedItem:
            self._selectedItem.CharInput(ch)
    
    def BackInput(self):
        if self._selectedItem:
            self._selectedItem.BackInput()

    def SelectCrossItem(self, button):
        if self._selectedItem in button.owners and len(button.owners) == 2:
            for item in button.owners:
                if item != self._selectedItem:
                    item.SetActiveState(True, button)
                    self.SetSelectedItem(item)
                    return True
        return False
    
    @FunctionTime
    def Generate(self):
        AppLog().Log(AppLog.CrosswordSystem, "Generate")
        if self._field:
            self._CleanField()
        else:
            self._GenerateField()
        self._AddFirstWord()
        self._AddOtherWords()
        self._SetInitialState()
    
    def CheckWords(self):
        result = {}
        for wordItem in self._crosswordItems:
            result[wordItem.GetWord()] = wordItem.Check()
        return result
    
    def IsFieldGenerated(self):
        return len(self._field) > 0
    
    def _DeselectItem(self):
        if self._selectedItem:
            self._selectedItem.SetActiveState(False)

    def _ShowHint(self):
        if not self._hintSetter:
            return
        if not self._selectedItem:
            self._hintSetter("")
            return
        meaning = Dictionary().GetUserMeaningsStr(self._selectedItem.GetWord())
        self._hintSetter(meaning)

    def _InitFilter(self):
        self._filter = WordFilter()
        self._filterCallback = lambda w: self._filter.CheckWord(w)

    @FunctionTime
    def _GenerateField(self):
        callback = lambda obj: self.CrosswordButtonPressed(obj)
        fieldGenerator = GridField(self._mainField, callback)
        self._field = fieldGenerator.GetField()
    
    def _SetInitialState(self):
        self.SetSelectedItem(None)
        for wordItem in self._crosswordItems:
            wordItem.SetInitialState()

    def _CleanField(self):
        for wordItem in self._crosswordItems:
            wordItem.CleanItems()
    
    def _AddFirstWord(self):
        self._generating = []
        self._crosswordItems = []
        maxSize = min(len(self._field), len(self._field[0]))
        self._filter.CleanFilter()
        self._filter.SetLen(max = maxSize)
        firstWord = Dictionary().GetNextWordByFilter(self._filterCallback)
        AppLog().Log(AppLog.CrosswordSystem, "AddFirstWord. word  = {0}".format(firstWord))
        if random.randint(0, 1):
            self._AddCrosswordItem(firstWord, random.choice(self._field))
        else:
            ind = random.randrange(0, len(self._field[0]))
            self._AddCrosswordItem(firstWord, self._GetVerticalLine(ind))
    
    def _AddCrosswordItem(self, word, items, startPos = -1):
        AppLog().Log(AppLog.CrosswordSystem, "AddCrosswordItem. word  = {0}".format(word))
        crosswordItem = CrosswordItem(word, items, startPos)
        self._filter.AddIgnore(word)
        self._crosswordItems.append(crosswordItem)
        crosswordItem.AddFirstItemMark(str(len(self._crosswordItems)))
        self._generating.extend(crosswordItem.GetItems())
    
    def _GetVerticalLine(self, index):
        if not self._field and index >= len(self._field[0]):
            return []
        return [el[index] for el in self._field]
    
    def _AddOtherWords(self):
        while(self._generating):
            if len(self._crosswordItems) > self._maxNumOfWords:
                break
            item = random.choice(self._generating)
            self._TryAddWord(item)
    
    def _TryAddWord(self, item):
        AppLog().Log(AppLog.CrosswordSystem, "TryAddWord. item  = {0}. X = {1} Y = {2}".format(item.text, item.indexX, item.indexY))
        if self._IsWordItemHorizontal(item):
            self._TryAddVerticalWord(item)
        else:
            self._TryAddHorizontalWord(item)
        self._RemoveFromGenerating(item)
    
    def _IsWordItemHorizontal(self, item):
        if item.owners:
            return item.owners[0].IsHorizontal()
        return False

    def _TryAddHorizontalWord(self, item):
        AppLog().Log(AppLog.CrosswordSystem, "TryAddHorizontalWord. item  = {0}. X = {1} Y = {2}".format(item.text, item.indexX, item.indexY))
        if self._IsHorizontalSpaceFree(item.indexX, item.indexY):
            self._AddWordByFilter(item, self._field[item.indexX], True)

    def _TryAddVerticalWord(self, item):
        AppLog().Log(AppLog.CrosswordSystem, "TryAddVerticalWord. item  = {0}. X = {1} Y = {2}".format(item.text, item.indexX, item.indexY))
        if self._IsVerticalSpaceFree(item.indexX, item.indexY):
            self._AddWordByFilter(item, self._GetVerticalLine(item.indexY), False)
    
    def _IsHorizontalSpaceFree(self, indX, indY):
        if self._IsItemFree(indX, indY + 1) and self._IsItemFree(indX, indY - 1):
            return True
        return False
    
    def _IsVerticalSpaceFree(self, indX, indY):
        if self._IsItemFree(indX + 1, indY) and self._IsItemFree(indX - 1, indY):
            return True
        return False

    def _IsItemFree(self, indX, indY):
        item = self._GetItem(indX, indY)
        if item and item.text != "":
            return False
        return True
    
    def _GetItem(self, indX, indY):
        if indX >= len(self._field) or indY >= len(self._field[0]):
            return None
        if indX < 0 or indY < 0:
            return None
        return self._field[indX][indY]

    def _GetFilterMarkForItem(self, indX, indY, isHorizontal):
        isFree = self._IsVerticalSpaceFree(indX, indY) if isHorizontal else self._IsHorizontalSpaceFree(indX, indY)
        mark = WordFilter.AnyItem if isFree else WordFilter.ForbiddenItem
        return mark
    
    def _GetFilterString(self, items, isHorizontal):
        filterStr = ""
        for item in items:
            if item.text:
                filterStr += item.text
            else:
                filterStr += self._GetFilterMarkForItem(item.indexX, item.indexY, isHorizontal)
        return filterStr

    def _AddWordByFilter(self, mainItem, items, isHorizontal):
        filterStr = self._GetFilterString(items, isHorizontal)
        index = items.index(mainItem)
        self._filter.SetFilter(filterStr, index)
        word = Dictionary().GetNextWordByFilter(self._filterCallback)
        AppLog().Log(AppLog.CrosswordSystem, "AddWordByFilter. word  = {0}".format(word))
        if word:
            startPos = index - self._filter.GetCenterIndex()
            self._AddCrosswordItem(word, items, startPos)
            self._RemSurroundedFromGenerating(mainItem)
    
    def _RemSurroundedFromGenerating(self, item):
        self._RemoveFromGenerating(self._GetItem(item.indexX + 1, item.indexY))
        self._RemoveFromGenerating(self._GetItem(item.indexX - 1, item.indexY))
        self._RemoveFromGenerating(self._GetItem(item.indexX, item.indexY + 1))
        self._RemoveFromGenerating(self._GetItem(item.indexX, item.indexY - 1))
    
    def _RemoveFromGenerating(self, item):
        if item and item in self._generating:
            self._generating.remove(item)
