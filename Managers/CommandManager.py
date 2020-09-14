import sys
import inspect
import Commands
import Logger

CONFIG_COMMANDS_KEY = 'commands'


class CommandManager():
    sensorManager = None
    commands = []

    def __init__(self, config, mqttClient, logger):
        self.config = config
        self.mqttClient = mqttClient
        self.logger = logger

    def InitializeCommands(self):
        self.LoadCommandsFromConfig()

    def PostInitializeCommands(self):
        for command in self.commands:
            try:
                command.PostInitialize()
            except Exception as exc:
                self.Log(Logger.LOG_ERROR, command.name +
                         ': error during post-initialization: '+str(exc))
                self.UnloadCommand(command.name)

    def LoadCommandsFromConfig(self):
        if CONFIG_COMMANDS_KEY in self.config:
            commandsToAdd = self.config[CONFIG_COMMANDS_KEY]
            for command in commandsToAdd:
                self.LoadCommand(command)

    def LoadCommand(self, commandString):
        name = commandString
        options = None

        # If in the list I have a dict then I have some options for that command
        if type(commandString) == dict:
            name = list(commandString.keys())[0]
            options = commandString[name]

        obj = self.GetCommandObjectByName(name)
        if(obj):
            self.commands.append(obj(self, options, self.logger))
            self.Log(Logger.LOG_INFO, name + ' command loaded')

    def UnloadCommand(self, name):
        obj = self.FindCommand(name)
        self.commands.remove(obj)
        self.Log(Logger.LOG_WARNING, name + ' command unloaded')

    def FindCommand(self, name):
        # Return the command object present in commands list: to get command value from another command for example
        for command in self.ActiveCommands():
            if name == command.name:  # If it's an object->obj.name, if a class must use the .__dict__ for the name
                return command
        return None

    def ActiveCommands(self):
        return self.commands

    def GetCommandObjectByName(self, name):
        commandList = self.GetCommandObjectsList()
        for command in commandList:
            if name == self.GetCommandName(command):
                return command
        self.Log(Logger.LOG_ERROR, str(name) + ' command not found')

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

    def Log(self, messageType, message):
        self.logger.Log(messageType, 'Command Manager', message)
