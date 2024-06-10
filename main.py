import kivy

from Tools.AppLog import AppLog
from Core.MainApp import MainApp

kivy.require('2.3.0')

if __name__ == '__main__':
    AppLog().InitListLoggers()
    app = MainApp()
    app.run()
    app.Shutdown()
