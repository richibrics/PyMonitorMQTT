import sys
import inspect
import Commands
import Logger


class CommandManager():
    # commands is a list of object (Command)
    commands = []
    sensorManager = None

    '''
    def __init__(self, config):
        self.config = config
        self.logger = Logger.Logger(config)


    def PostInitializeCommands(self):
        for command in self.commands:
            try:
                command.PostInitialize()
            except Exception as exc:
                self.Log(Logger.LOG_ERROR, command.name +
                         ': error during post-initialization: '+str(exc))
                self.Log(Logger.LOG_ERROR,
                         Logger.ExceptionTracker.TrackString(exc))
                self.UnloadCommand(command.name, command.GetMonitorID())


    # Here I receive the name of the command (or maybe also the options) and pass it to a function to get the object
    # which will be initialized and appended in the list of commands
    # Here configs are specific for the monitor, it's not the same as this manager
    def LoadCommand(self, commandString, monitor_id, config, mqtt_client, logger):
        name = commandString
        options = None

        # If in the list I have a dict then I have some options for that command
        if type(commandString) == dict:
            name = list(commandString.keys())[0]
            options = commandString[name]

        obj = self.GetCommandObjectByName(name)
        if(obj):
            # Initialize here object and append it
            try:
                objAlive = obj(monitor_id, config, mqtt_client,
                               options, logger, self)
                self.commands.append(objAlive)
                req = objAlive.LoadSettings()
                self.Log(Logger.LOG_INFO, name +
                         ' command loaded', logger=logger)
                return req  # Return the settings with requirements
            except Exception as exc:
                self.Log(Logger.LOG_ERROR, name +
                         ' command occured an error during loading', logger=logger)
                self.Log(Logger.LOG_ERROR, Logger.ExceptionTracker.TrackString(
                    exc), logger=logger)
        return None

    def UnloadCommand(self, name, monitor_id):
        command = self.FindCommand(name, monitor_id)
        self.Log(Logger.LOG_WARNING, name +
                 ' command unloaded', logger=command.GetLogger())
        self.commands.remove(command)

    def FindCommand(self, name, monitor_id):
        # Return the command object present in commands list: to get command value from another command for example
        for command in self.ActiveCommands():
            # If it's an object->obj.name, if a class must use the .__dict__ for the name
            if name == command.name and monitor_id == command.GetMonitorID():
                return command
        return None

    def ActiveCommands(self):
        return self.commands

    
    def GetCommandObjectByName(self, name):
        commandList = self.GetCommandObjectsList()
        for command in commandList:
            if name == self.GetCommandName(command):
                return command
        self.Log(Logger.LOG_ERROR, str(name) + ' command not found - check the module import line is added to Commands/__init__.py')

    
    def GetCommandObjectsList(self):
        classes = []
        for name, obj in inspect.getmembers(sys.modules['Commands']):
            if inspect.isclass(obj):
                # Don't add Command parent class to the list
                if('.Command' not in self.GetClassName(obj)):
                    classes.append(obj)
        return classes

    
    def GetClassName(self, command_class):
        # Commands.COMMANDFOLDER.COMMANDCLASS
        return command_class.__dict__['__module__']

    def GetCommandName(self, command_class):
        # Only COMMANDCLASS (without Command suffix)
        return self.GetClassName(command_class).split('.')[-1].split('Command')[0]

    def SetSensorManager(self, sensorManager):
        self.sensorManager = sensorManager

    def Log(self, messageType, message, logger=None):
        if logger is None:
            logger = self.logger
        logger.Log(messageType, 'Command Manager', message)

    '''