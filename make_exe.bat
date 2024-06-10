@echo off

python --version
if ERRORLEVEL 1 goto NOPYTHON

python --version | findstr /L /C:"Python 3"
if ERRORLEVEL 1 goto NOPYTHON

pip --version
if ERRORLEVEL 1 goto NOPIP

pip show pyinstaller
if ERRORLEVEL 1 goto NOPYINSTALLER

goto :MAKEEXE

:NOPYTHON
echo Error
echo Python 3 is required to continue
goto :eof

:NOPIP
echo Error
echo Pip is required to continue
goto :eof

:NOPYINSTALLER

pip install pyinstaller

:MAKEEXE

pip install -r requirements.txt

python -m PyInstaller --onefile --distpath bin --name "Learner Word" --icon Data\Logo\logo.png main.py
xcopy /s Data bin\Data\
