from kivy.core.audio import SoundLoader

from Tools.ThreadManager import ThreadManager

from enum import Enum
from gtts import gTTS
import os

class SoundState(Enum):
    Initialization = 0
    Idle = 1
    Playing = 2
    Waiting = 3
    Error = 4

class Sound:
    def __init__(self, name, lang) -> None:
        self._name = name
        self._lang = lang
        self._sound = None
        self._state = SoundState.Initialization
        self._folder = os.path.join("Data", "Sounds", self._lang)
        self._fileExt = ".mp3"
        self._maxNameLen = 100
        self._filePath = self._GetFilePath(self._name)
        ThreadManager().RunNewThread("loading", self._Load, self._LoadFinished)

    def Play(self):
        if self._state == SoundState.Initialization:
            self._SetState(SoundState.Waiting)
        elif self._state == SoundState.Idle:
            self._StartPlay()
    
    def _StartPlay(self):
        self._SetState(SoundState.Playing)
        ThreadManager().RunNewThread("playing", self._Play, self._PlayFinished)

    def _Play(self):
        if self._sound.state == "play":
            self._sound.stop()
        self._sound.play()
        self._sound.seek(0)
    
    def _Load(self):
        forceDownload = len(self._name) > self._maxNameLen
        if forceDownload or not os.path.isfile(self._filePath):
            self._DownloadSound()
        if self._SetState == SoundState.Error:
            return
        try:
            self._sound = SoundLoader.load(self._filePath)
        except:
            self._SetState(SoundState.Error)
    
    def _DownloadSound(self):
        try:
            tts = gTTS(self._name, lang = self._lang)
            folder = os.path.join(self._folder, self._name[0])
            if not os.path.exists(folder):
                os.makedirs(folder)
            tts.save(self._filePath)
        except:
            self._SetState(SoundState.Error)

    def _LoadFinished(self):
        if not self._sound:
            self._SetState(SoundState.Error)
        elif self._state == SoundState.Waiting:
            self._StartPlay()
        elif self._state == SoundState.Initialization:
            self._SetState(SoundState.Idle)
    
    def _PlayFinished(self):
        if self._state == SoundState.Playing:
            self._SetState(SoundState.Idle)

    def _GetFilePath(self, name):
        if name:
            return os.path.join(self._folder, name[0], name[:self._maxNameLen] + self._fileExt)
        return ""
    
    def _SetState(self, state):
        self._state = state
