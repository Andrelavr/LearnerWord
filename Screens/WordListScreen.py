from kivy.properties import ObjectProperty

from Dictionary.Dictionary import Dictionary
from Dictionary.Level import Level
from Screens.UIElements import CustomScreen
from Screens.WordItemInfo import WordItemInfo
from Screens.UIElements import TrainingWordMenu
from Screens.UIElements import LearnedWordMenu
from Screens.UIElements import IgnoreWordMenu

class WordListScreen(CustomScreen):
    
    recycleView = ObjectProperty(None)
    itemBubble = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []
        self._sortByWordRev = False
        self._sortByGamesRev = True
        self._sortByWinGamesRev = True
        self._sortByFailGamesRev = True
        self._sortBySeriesGamesRev = True
        self._currentLevel = Level.LevelInTraining
        self._wordBubbleWidth = 0.8
    
    def on_pre_enter(self, *args):
        super().on_pre_enter(self, *args)
        self._PopulateData()
        self.recycleView.data = self.data
    
    def on_leave(self, *args):
        super().on_leave(self, *args)
        self._ResetBubble()

    def SortByWord(self):
        self.recycleView.data = sorted(self.data, key = lambda el: el.get("text"), reverse = self._sortByWordRev)
        self._sortByWordRev = not self._sortByWordRev

    def SortByGames(self):
        self.recycleView.data = sorted(self.data, key = lambda el: int(el.get("games")), reverse = self._sortByGamesRev)
        self._sortByGamesRev = not self._sortByGamesRev

    def SortByWinGames(self):
        self.recycleView.data = sorted(self.data, key = lambda el: int(el.get("correct")), reverse = self._sortByWinGamesRev)
        self._sortByWinGamesRev = not self._sortByWinGamesRev

    def SortByFailGames(self):
        self.recycleView.data = sorted(self.data, key = lambda el: int(el.get("wrong")), reverse = self._sortByFailGamesRev)
        self._sortByFailGamesRev = not self._sortByFailGamesRev

    def SortBySeriesGames(self):
        self.recycleView.data = sorted(self.data, key = lambda el: int(el.get("series")), reverse = self._sortBySeriesGamesRev)
        self._sortBySeriesGamesRev = not self._sortBySeriesGamesRev
    
    def SetLevelNewWords(self):
        self._currentLevel = Level.LevelNewWords
    
    def SetLevelInTraining(self):
        self._currentLevel = Level.LevelInTraining
    
    def SetLevelLearned(self):
        self._currentLevel = Level.LevelLearned
    
    def SetLevelIgnore(self):
        self._currentLevel = Level.LevelIgnore
    
    def MoveWordToIgnore(self, word):
        Dictionary().SetWordLevel(word, Level.LevelIgnore)
        self._RemoveWordFromList(word)

    def MoveWordToTraining(self, word):
        Dictionary().SetWordLevel(word, Level.LevelInTraining)
        self._RemoveWordFromList(word)

    def MoveWordToLearned(self, word):
        Dictionary().SetWordLevel(word, Level.LevelLearned)
        self._RemoveWordFromList(word)
    
    def Remove(self, word):
        Dictionary().RemoveWord(word)
        self._RemoveWordFromList(word)
    
    def ButtonWordPressed(self, text, item, button):
        if not self._IsBubbleExist():
            WordListScreen.itemBubble = WordItemInfo(word = text)
            self._UpdateBubblePos(item, button.last_touch, True)
            WordListScreen.itemBubble.width = self.width * self._wordBubbleWidth
            self.recycleView.children[0].add_widget(WordListScreen.itemBubble)
        else:
            self._ResetBubble()

    def ButtonGamesPressed(self):
        self._ResetBubble()

    def ButtonCorrectPressed(self):
        self._ResetBubble()

    def ButtonWrongPressed(self):
        self._ResetBubble()

    def ButtonSeriesPressed(self):
        self._ResetBubble()

    def ButtonMorePressed(self, text, item, button):
        if not self._IsBubbleExist():
            self._CreateMenuBubble(text)
            self._UpdateBubblePos(item, button.last_touch, False)
            self.recycleView.children[0].add_widget(WordListScreen.itemBubble)
        else:
            self._ResetBubble()
    
    def _CreateMenuBubble(self, text):
        level = Dictionary().GetWordLevel(text)
        if level == Level.LevelIgnore:
            WordListScreen.itemBubble = IgnoreWordMenu()
        elif level == Level.LevelLearned:
            WordListScreen.itemBubble = LearnedWordMenu()
        else:
            WordListScreen.itemBubble = TrainingWordMenu()
        WordListScreen.itemBubble.word = text
    
    def _IsBubbleExist(self):
        if WordListScreen.itemBubble:
            if WordListScreen.itemBubble.parent:
                return True
        return False
    
    def _ResetBubble(self):
        if self._IsBubbleExist():
            WordListScreen.itemBubble.parent.remove_widget(WordListScreen.itemBubble)
        WordListScreen.itemBubble = None
    
    def _UpdateBubblePos(self, item, touch, toLeft):
        posX = item.x if toLeft else item.width - WordListScreen.itemBubble.width 
        if touch.sy > 0.5:
            WordListScreen.itemBubble.pos = (posX, item.y - WordListScreen.itemBubble.height)
            WordListScreen.itemBubble.arrow_pos = 'top_mid'
        else:
            WordListScreen.itemBubble.pos = (posX, item.y + item.height)
            WordListScreen.itemBubble.arrow_pos = 'bottom_mid'
        WordListScreen.itemBubble.adjust_position()

    def _RemoveWordFromList(self, word):
        self.recycleView.data = filter(lambda el: el.get("text") != word, self.recycleView.data)

    def _PopulateData(self):
        dictionary = Dictionary()
        words = dictionary.GetWordsByLevel(self._currentLevel)
        self.data.clear()
        for word in words:
            games = str(dictionary.GetNumOfGames(word))
            wrong = str(dictionary.GetNumOfWrongAns(word))
            correct = str(dictionary.GetNumOfCorrectAns(word))
            series = str(dictionary.GetLastLenWinSeries(word))
            self.data.append({"text":word, "games":games, "wrong":wrong, "correct":correct, "series":series})
