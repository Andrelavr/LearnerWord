class LabelTextConverter:

    def __init__(self) -> None:
        self._refTemplate = "[ref={0}]{1}[/ref]"
        self._textColor = "ffffff"
        self._coloredTagTemplate = "[color={0}]"
        self._coloredTagStart = self._coloredTagTemplate.format(self._textColor)
        self._coloredTagEnd = "[/color]"
        self._minLenOfWord = 2
        self._text = []
    
    def SetTextColor(self, color):
        self._textColor = color
        self._coloredTagStart = self._coloredTagTemplate.format(self._textColor)
    
    def IsWordColored(self, index) -> bool:
        start = "".join(self._text[index - len(self._coloredTagStart):index])
        end = "".join(self._text[index + 1:index + 1 + len(self._coloredTagEnd)])
        if start == self._coloredTagStart and end == self._coloredTagEnd:
            return True
        return False
    
    def ToggleWordColorTag(self, index, enableTag):
        if index < 0 or index >= len(self._text):
            return
        if enableTag:
            text = self._text[:index]
            text.extend(self._coloredTagStart)
            text.append(self._text[index])
            text.extend(self._coloredTagEnd)
            text.extend(self._text[index + 1:])
            self._text = text
            return
        self._text = self._text[:index + 1] + self._text[index + 1 + len(self._coloredTagEnd):]
        self._text = self._text[:index - len(self._coloredTagStart)] + self._text[index:]

    def MakeRefs(self, text) -> str:
        elements = self._ParseText(text, self._ConvertWordToRef)
        return "".join(elements)
    
    def SetText(self, text):
        self._text = self._ParseText(text, self._WordFromList)
    
    def GetConvertedText(self) -> str:
        converted = []
        for ind, word in enumerate(self._text):
            converted.extend(self._ConvertWordToIndexedRef(ind, word))
        return "".join(converted)
    
    def MakeRefsFromList(self, textElements) -> str:
        refElements = []
        for text in textElements:
            refElements.append(self._ConvertWordToRef(text))
        return refElements
    
    def MakeRef(self, text) -> str:
        return self._ConvertWordToRef(text)
    
    def ParseIndexedRef(self, text) -> tuple[int, str]:
        pointIndex = text.find('.')
        if pointIndex == -1:
            return (0, text)
        textPart = text[pointIndex + 1:]
        indexPart = text[:pointIndex]
        if indexPart.isdecimal():
            return (int(indexPart), textPart)
        return (0, textPart)
    
    def _ParseText(self, text, parseFunc) -> list:
        word = []
        textElements = []
        for ch in text:
            if ch.isalpha():
                word.append(ch)
            else:
                textElements.extend(parseFunc(word))
                textElements.append(ch)
                word.clear()
        textElements.extend(parseFunc(word))
        return textElements
    
    def _WordFromList(self, word):
        if len(word) >= self._minLenOfWord:
            return ["".join(word)]
        return word

    def _ConvertWordToRef(self, word):
        if len(word) >= self._minLenOfWord:
            wordStr = "".join(word)
            return self._refTemplate.format(wordStr, wordStr)
        return word
    
    def _ConvertWordToIndexedRef(self, index, word):
        if len(word) >= self._minLenOfWord:
            wordStr = "".join(word)
            ref = "{0}.{1}".format(index, wordStr)
            return [self._refTemplate.format(ref, wordStr)]
        return word
