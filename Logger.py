import datetime
import os
import sys
from consts import *
import json
from Configurator import Configurator

# Fill start of string with spaces to jusitfy the message (0: no padding)
# First for type, second for monitor, third for source
STRINGS_LENGTH = [8, 12, 26]

# Number of spaces between prestring (date,source,ecc..) and message
PRESTRING_MESSAGE_SEPARATOR_LEN = 2
LONG_MESSAGE_PRESTRING_CHAR = ' '

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

scriptFolder = str(os.path.dirname(os.path.realpath(__file__)))
LOGS_FOLDER = 'Logs'
MAIN_LOG_FILENAME = 'Log.log'


class Logger():
    LOG_MESSAGE = 0
    LOG_ERROR = 1
    LOG_WARNING = 2
    LOG_INFO = 3
    LOG_DEBUG = 4
    LOG_DEVELOPMENT = 5

    def __init__(self, globalConfig, monitor_id=None):
        self.globalConfig = globalConfig
        self.monitor_id = monitor_id
        self.GetConfiguration()
        self.SetupFolder()

    def Log(self, messageLevel, source, message):
        if type(message) == dict:
            self.LogDict(messageLevel,source,message)
            return # Log dict will call this function so I don't need to go down at the moment
        elif type(message) == list:
            self.LogList(messageLevel,source,message)
            return # Log list will call this function so I don't need to go down at the moment

        if messageLevel == self.LOG_INFO:
            messageType = 'Info'
        elif messageLevel == self.LOG_ERROR:
            messageType = 'Error'
        elif messageLevel == self.LOG_WARNING:
            messageType = 'Warning'
        elif messageLevel == self.LOG_DEBUG:
            messageType = 'Debug'
        elif messageLevel == self.LOG_MESSAGE:
            messageType = 'Message'
        elif messageLevel == self.LOG_DEVELOPMENT:
            messageType = 'Dev'
        else:
            messageType = 'Logger'

        if self.monitor_id is None:  # It's not the logger for a monitor
            monitor_text = 'Main'
        else:
            monitor_text = 'Monitor #' + str(self.monitor_id)

        prestring = '[ '+self.GetDatetimeString()+' | '+messageType.center(STRINGS_LENGTH[0]) + ' | '+monitor_text.center(STRINGS_LENGTH[1]) + \
            ' | '+source.center(STRINGS_LENGTH[2])+']' + \
            PRESTRING_MESSAGE_SEPARATOR_LEN*' '  # justify

        # Manage string to print in more lines if it's too long
        while len(message) > 0:
            string = prestring+message[:self.logger_message_width]
            # Cut for next iteration if message is longer than a line
            message = message[self.logger_message_width:]
            if(len(message) > 0):
                string = string+'-'  # Print new line indicator if I will go down in the next iteration
            self.PrintAndSave(string, messageLevel)
            # -1 + space cause if the char in the prestring isn't a space, it will be directly attached to my message without a space

            prestring = (len(prestring)-PRESTRING_MESSAGE_SEPARATOR_LEN) * \
                LONG_MESSAGE_PRESTRING_CHAR+PRESTRING_MESSAGE_SEPARATOR_LEN*' '

    
    def LogDict(self, messageLevel, source, dict):
        try:
            string = json.dumps(dict, indent=4, sort_keys=False, default=lambda o: '<not serializable>')
            lines=string.splitlines()
            for line in lines:
                self.Log(messageLevel,source,"> "+line)
        except Exception as e:
            self.Log(self.LOG_ERROR,source,"Can't print dictionary content")

    def LogList(self, messageLevel, source, _list):
        try:
            for index, item in enumerate(_list):
                if type(item)==dict or type(item)==list:
                    self.Log(messageLevel,source,"Item #"+str(index))
                    self.Log(messageLevel,source, item)
                else:
                    self.Log(messageLevel,source,str(index) + ": " + str(item))

        except:
            self.Log(self.LOG_ERROR,source,"Can't print dictionary content")


    def SetupFolder(self):
        if not os.path.exists(os.path.join(scriptFolder, LOGS_FOLDER)):
            os.mkdir(os.path.join(scriptFolder, LOGS_FOLDER))

    def GetDatetimeString(self):
        now = datetime.datetime.now()
        return now.strftime(DATETIME_FORMAT)

    def PrintAndSave(self, string, level):
        if level <= self.console_log_level:
            print(string)
        if level <= self.file_log_level:
            with open(os.path.join(scriptFolder, LOGS_FOLDER, MAIN_LOG_FILENAME), "a") as logFile:
                logFile.write(string+' \n')

    def GetConfiguration(self):
        # Message width
        self.logger_message_width = Configurator.GetOption(self.globalConfig, [
                                                           LOGGER_CONFIG_KEY, LOGGER_MESSAGE_WIDTH_KEY], LOGGER_MESSAGE_WIDTH_DEFAULT)
        # File level
        self.file_log_level = Configurator.GetOption(
            self.globalConfig, [LOGGER_CONFIG_KEY, LOGGER_FILE_LEVEL_KEY], LOGGER_DEFAULT_LEVEL)
        # Console level
        self.console_log_level = Configurator.GetOption(self.globalConfig, [
                                                        LOGGER_CONFIG_KEY, LOGGER_CONSOLE_LEVEL_KEY], LOGGER_DEFAULT_LEVEL)


class ExceptionTracker():

    # Call this static method inside an except block
    def Track():
        # Return file and line where exception occured
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        return {'filename': filename, 'line': line_number}

    # Call this static method inside an except block, will return a formatted string with data
    def TrackString(exception):
        data = ExceptionTracker.Track()
        message = str(exception)
        return "Critical error in '{}' at line {}: {}".format(data['filename'], data['line'], message)
