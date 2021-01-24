import datetime
import os
import sys
from consts import *

LOG_MESSAGE = 0
LOG_ERROR = 1
LOG_WARNING = 2
LOG_INFO = 3
LOG_DEBUG = 4
LOG_DEVELOPMENT = 5

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
    def __init__(self, globalConfig, monitor_id=None):
        self.globalConfig = globalConfig
        self.monitor_id = monitor_id
        self.GetConfiguration()
        self.SetupFolder()

    def Log(self, messageLevel, source, message):
        if messageLevel == LOG_INFO:
            messageType = 'Info'
        elif messageLevel == LOG_ERROR:
            messageType = 'Error'
        elif messageLevel == LOG_WARNING:
            messageType = 'Warning'
        elif messageLevel == LOG_DEBUG:
            messageType = 'Debug'
        elif messageLevel == LOG_MESSAGE:
            messageType = 'Message'
        elif messageLevel == LOG_DEVELOPMENT:
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
            self.PrintAndSave(string,messageLevel)
            # -1 + space cause if the char in the prestring isn't a space, it will be directly attached to my message without a space
            prestring = (len(prestring)-PRESTRING_MESSAGE_SEPARATOR_LEN) * \
                LONG_MESSAGE_PRESTRING_CHAR+PRESTRING_MESSAGE_SEPARATOR_LEN*' '

    def SetupFolder(self):
        if not os.path.exists(os.path.join(scriptFolder, LOGS_FOLDER)):
            os.mkdir(os.path.join(scriptFolder, LOGS_FOLDER))

    def GetDatetimeString(self):
        now = datetime.datetime.now()
        return now.strftime(DATETIME_FORMAT)

    def PrintAndSave(self, string,level):
        if level <= self.console_log_level:
            print(string)
        if level <= self.file_log_level:
            with open(os.path.join(scriptFolder, LOGS_FOLDER, MAIN_LOG_FILENAME), "a") as logFile:
                logFile.write(string+' \n')

    def GetConfiguration(self):
        if self.globalConfig:
            if LOGGER_CONFIG_KEY in self.globalConfig:

                # Message width
                if LOGGER_MESSAGE_WIDTH_KEY in self.globalConfig[LOGGER_CONFIG_KEY]:
                    self.logger_message_width = self.globalConfig[LOGGER_CONFIG_KEY][LOGGER_MESSAGE_WIDTH_KEY]
                else:
                    self.logger_message_width = LOGGER_MESSAGE_WIDTH_DEFAULT

                # File level
                if LOGGER_FILE_LEVEL_KEY in self.globalConfig[LOGGER_CONFIG_KEY]:
                    self.file_log_level = self.globalConfig[LOGGER_CONFIG_KEY][LOGGER_FILE_LEVEL_KEY]
                else:
                    self.file_log_level = LOGGER_DEFAULT_LEVEL

                # Console level
                if LOGGER_CONSOLE_LEVEL_KEY in self.globalConfig[LOGGER_CONFIG_KEY]:
                    self.console_log_level = self.globalConfig[LOGGER_CONFIG_KEY][LOGGER_CONSOLE_LEVEL_KEY]
                else:
                    self.console_log_level = LOGGER_DEFAULT_LEVEL
                

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
