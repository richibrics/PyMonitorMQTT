import datetime
import os

LOG_INFO = 0
LOG_ERROR = 1
LOG_WARNING = 2
LOG_DEBUG = 3

# Fill start of string with spaces to jusitfy the message (0: no padding)
STRINGS_LENGTH = [7, 26]  # First for type, second for source

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

scriptFolder = str(os.path.dirname(os.path.realpath(__file__)))
LOGS_FOLDER = 'Logs'
MAIN_LOG_FILENAME = 'Log.log'


class Logger():
    def __init__(self):
        self.SetupFolder()

    def Log(self, messageType, source, message):
        if messageType == LOG_INFO:
            messageType = 'Info'
        elif messageType == LOG_ERROR:
            messageType = 'Error'
        elif messageType == LOG_WARNING:
            messageType = 'Warning'
        elif messageType == LOG_DEBUG:
            messageType = 'Debug'
        else:
            messageType = 'Logger'

        prestring = '[ '+self.GetDatetimeString()+' | '+messageType.center(STRINGS_LENGTH[0]) + \
            ' | '+source.center(STRINGS_LENGTH[1])+']  '  # justify
        string = prestring+message

        print(string)
        with open(os.path.join(scriptFolder, LOGS_FOLDER, MAIN_LOG_FILENAME), "a") as logFile:
            logFile.write(string+'\n')

    def SetupFolder(self):
        if not os.path.exists(os.path.join(scriptFolder, LOGS_FOLDER)):
            os.mkdir(os.path.join(scriptFolder, LOGS_FOLDER))

    def GetDatetimeString(self):
        now = datetime.datetime.now()
        return now.strftime(DATETIME_FORMAT)
