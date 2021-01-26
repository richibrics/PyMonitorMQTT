import os
import consts
import json

class Settings():
    def GetInformation():
        if os.path.exists(consts.INFORMATION_FILENAME):
            with open(consts.INFORMATION_FILENAME,"r") as f:
                return json.loads(f.read())