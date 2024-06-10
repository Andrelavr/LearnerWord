import requests
import urllib
import time
import json

class GoogleTranslator:
    def __init__(self):
        self._url = 'https://translate.google.com'
        self._apiUrl = '/_/TranslateWebserverUi/data/batchexecute'
        self._translateUrl = f'{self._url}{self._apiUrl}'
        self._userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        self._rpcid = 'MkEWBc'
        self._beginTime = time.time()
        self._maxLenOfSessionInSeconds = 1500
        self._hostHeader = self._GetHostHeader()
        self._apiHeader = self._GetApiHeader()
        self._session = None

    def Translate(self, text: str, fromLanguage: str, toLanguage: str) -> list:
        fromLang = GoogleTranslator.languages.get(fromLanguage, "en")
        toLang = GoogleTranslator.languages.get(toLanguage, "en")
        if fromLang == toLang:
            return []
        self._CreateSession()
        rpcData = self._GetRpc(text, fromLang, toLang)
        rpcData = urllib.parse.urlencode(rpcData)
        response = self._session.post(self._translateUrl, headers = self._apiHeader, data = rpcData)
        response.raise_for_status()
        jsonData = json.loads(response.text[6:])
        data = json.loads(jsonData[0][2])
        return data
    
    def _GetHostHeader(self):
        hostHeader = {
            'Referer': self._url,
            "User-Agent": self._userAgent,
        }
        return hostHeader
    
    def _GetApiHeader(self):
        apiHeader = {
            'Origin': self._url,
            'Referer': self._url,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "User-Agent": self._userAgent,
        }
        return apiHeader

    def _GetRpc(self, text: str, fromLanguage: str, toLanguage: str) -> dict:
        param = json.dumps([[text, fromLanguage, toLanguage, True], [1]])
        rpc = json.dumps([[[self._rpcid, param, None, "generic"]]])
        return {'f.req': rpc}
    
    def _CreateSession(self):
        needUpdate = time.time() - self._beginTime < self._maxLenOfSessionInSeconds
        if self._session == None or needUpdate:
            self._beginTime = time.time()
            self._session = requests.Session()
            self._session.get(self._url, headers = self._hostHeader)

    languages = {
        "english":"en",
        "chinese":"zh",
        "arabic":"ar",
        "russian":"ru",
        "french":"fr",
        "german":"de",
        "spanish":"es",
        "portuguese":"pt",
        "italian":"it",
        "japanese":"ja",
        "korean":"ko",
        "greek":"el",
        "dutch":"nl",
        "hindi":"hi",
        "turkish":"tr",
        "malay":"ms",
        "thai":"th",
        "vietnamese":"vi",
        "indonesian":"id",
        "polish":"pl",
        "mongolian":"mn",
        "czech":"cs",
        "hungarian":"hu",
        "estonian":"et",
        "bulgarian":"bg",
        "danish":"da",
        "finnish":"fi",
        "romanian":"ro",
        "swedish":"sv",
        "slovenian":"sl",
        "persian/farsi":"fa",
        "bosnian":"bs",
        "serbian":"sr",
        "filipino":"tl",
        "haitiancreole":"ht",
        "catalan":"ca",
        "croatian":"hr",
        "latvian":"lv",
        "lithuanian":"lt",
        "urdu":"ur",
        "ukrainian":"uk",
        "welsh":"cy",
        "swahili":"sw",
        "samoan":"sm",
        "slovak":"sk",
        "afrikaans":"af",
        "norwegian":"no",
        "bengali":"bn",
        "malagasy":"mg",
        "maltese":"mt",
        "gujarati":"gu",
        "tamil":"ta",
        "telugu":"te",
        "punjabi":"pa",
        "amharic":"am",
        "azerbaijani":"az",
        "belarusian":"be",
        "cebuano":"ceb",
        "esperanto":"eo",
        "basque":"eu",
        "irish":"ga"
    }
