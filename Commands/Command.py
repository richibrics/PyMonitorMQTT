from consts import *
import Logger


class Command():
    topic = ""

    def __init__(self, commandManager, logger):  # Config is args
        self.commandManager = commandManager
        self.name = self.GetCommandName()
        self.logger = logger
        self.Initialize()

    # Implemented in sub-classes
    def Initialize(self):
        pass

    def CallCallback(self, message):  # Safe method to run the Callback
        try:
            self.Log(Logger.LOG_INFO, 'Command actioned')
            self.Callback(message)
        except Exception as exc:
            self.Log(Logger.LOG_ERROR, 'Error occured in callback: '+str(exc))
            self.commandManager.UnloadCommand(self.name)

    # Implemented in sub-classes
    def Callback(self, message):  # Run by the OnMessageEvent
        pass

    def SubscribeToTopic(self, topic):
        self.commandManager.mqttClient.AddNewTopic(topic, self)
        # Log the topic as debug if user wants
        if 'print_topics' in self.commandManager.config and self.commandManager.config['print_topics'] is True:
            self.Log(Logger.LOG_DEBUG, 'Subscribben to topic: ' + topic)

    def GetTopic(self, last_part_of_topic):
        model = TOPIC_FORMAT
        if 'topic_prefix' in self.commandManager.config:
            model = self.commandManager.config['topic_prefix'] + \
                '/'+model
        return model.format(self.commandManager.config['name'], last_part_of_topic)

    def GetClassName(self):
        # Command.SENSORFOLDER.SENSORCLASS
        return self.__class__.__name__

    def GetCommandName(self):
        # Only SENSORCLASS (without Command suffix)
        return self.GetClassName().split('.')[-1].split('Command')[0]

    def Log(self, messageType, message):
        self.logger.Log(messageType, self.name+' Command', message)
