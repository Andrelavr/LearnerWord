import json
import os
import gzip

class DataReader:

    def __init__(self, filename = "data", compressEnabled = False):
        self._dataFile = "Data/" + filename + ".json"
        self._backupFile = "Data/" + filename + ".bckp"
        self._tempFile = "Data/" + filename + ".temp"
        self._compressEnabled = compressEnabled

    def Read(self):
        data = self._ReadFile(self._dataFile, self._compressEnabled)
        if data:
            tempData = self._ReadFile(self._tempFile, self._compressEnabled)
            if tempData:
                data = tempData
                self._RenameFile(self._dataFile, self._backupFile)
                self._RenameFile(self._tempFile, self._dataFile)
                self._RemoveFile(self._backupFile)
        else:
            tempData = self._ReadFile(self._tempFile, self._compressEnabled)
            if tempData:
                data = tempData
                self._RenameFile(self._tempFile, self._dataFile)
                self._RemoveFile(self._tempFile)
            else:
                backupData = self._ReadFile(self._backupFile, self._compressEnabled)
                if backupData:
                    data = backupData
                    self._RenameFile(self._backupFile, self._dataFile)
                    self._RemoveFile(self._backupFile)
                else:
                    return None
        return data

    def Write(self, obj : dict):
        self._WriteData(self._tempFile, obj)
        self._RenameFile(self._dataFile, self._backupFile)
        self._RenameFile(self._tempFile, self._dataFile)
        self._RemoveFile(self._backupFile)

    def _WriteData(self, fileName, data):
        try:
            mode = "wb" if self._compressEnabled else "w"
            with open(fileName, mode) as file:
                if self._compressEnabled:
                    jsonData = json.dumps(data).encode()
                    compressedData = gzip.compress(jsonData)
                    file.write(compressedData)
                else:
                    json.dump(data, file, indent = 2)
            return True
        except:
            return False

    def _RenameFile(self, srcFile, dstFile):
        try:
            os.rename(srcFile, dstFile)
            return True
        except:
            return False
        
    def _RemoveFile(self, remFile):
        try:
            os.remove(remFile)
            return True
        except:
            return False
        
    def _ReadFile(self, fileName, compressEnabled, retryIfError = True):
        try:
            if not os.path.isfile(fileName):
                return None
            mode = "rb" if compressEnabled else "r"
            with open(fileName, mode) as file:
                if compressEnabled:
                    compressedData = file.read()
                    jsonData = gzip.decompress(compressedData).decode()
                    data = json.loads(jsonData)
                else:
                    data = json.load(file)
                if len(data) > 0:
                    return data
            return None
        except:
            if retryIfError:
                return self._ReadFile(fileName, not compressEnabled, False)
            return None
