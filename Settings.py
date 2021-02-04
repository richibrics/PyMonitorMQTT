import os
import consts
import json

class Settings():
    def GetMainFolder():
        return str(os.path.dirname(os.path.realpath(__file__)))
        
    def GetInformation():
        path = os.path.join(Settings.GetMainFolder(),consts.INFORMATION_FILENAME)
        if os.path.exists(path):
            with open(path,"r") as f:
                return json.loads(f.read())