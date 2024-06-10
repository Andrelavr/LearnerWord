import eng_to_ipa

#######################################################
#   term    [transcription]     meaning1, meaning2
#   term                        meaning1, meaning2
#######################################################

class WordsReader:
     
    def __init__(self, wordsData) -> None:
        self._fileWords = "Data/words.txt"
        self._wordsData = wordsData
        self._termSeparator = "   "
        self._meaningSeparator = ","

    def Read(self):
        lines = []
        with open(self._fileWords, encoding="utf8") as file:
            lines = file.readlines()
        for line in lines:
            self._ParseLine(line)
    
    def _ParseLine(self, line):
        listWords = line.split(self._termSeparator)
        listWords = [el.lstrip().rstrip() for el in listWords if el != '']
        word = ''
        transcription = ''
        translationStr = ''
        if len(listWords) > 1:
            if len(listWords[0]) > 0:
                word = listWords[0]
            if listWords[1].startswith('['):
                transcription = listWords[1]
            else:
                transcription = '[' + eng_to_ipa.convert(word) + ']'
                translationStr = listWords[1]
            if len(listWords) > 2:
                translationStr = listWords[2]
        if word and translationStr:
            translation = [tr.lstrip() for tr in translationStr.split(self._meaningSeparator)]
            self._AddWordData(word, transcription, translation)
    
    def _AddWordData(self, word, transcription, translation):
        if self._wordsData.IsItemDataExist(word):
            self._wordsData.UpdateMeaning(word, translation)
            self._wordsData.UpdateTranscription(word, transcription)
        else:
            self._wordsData.AddWord(word, transcription, translation)
