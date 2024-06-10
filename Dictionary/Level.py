class Level:
    LevelNewWords   = 0
    LevelInTraining = 1
    LevelLearned   = 2
    LevelIgnore    = 3

    @staticmethod
    def IsCorrectLevel(level):
        if level >= Level.LevelNewWords and level <= Level.LevelIgnore:
            return True
        return False
