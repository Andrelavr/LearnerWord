from Tools.AppLog import AppLog

import time

def FunctionTime(function):
    def inn(*args, **kwargs):
        begin = time.time()

        res = function(*args, **kwargs)
        
        end = time.time()
        AppLog().Log(AppLog.FuncTime, function.__name__ + " duration = " + str(end - begin))
        return res
        
    return inn
