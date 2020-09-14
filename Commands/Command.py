from consts import *
import Logger


class Command():
    #topic = ""

    def __init__(self, commandManager, options, logger):  # Config is args
        self.commandManager = commandManager
        self.name = self.GetCommandName()
        self.options = options
        self.logger = logger
        self.subscribedTopics = 0
        self.Initialize()

    # Implemented in sub-classes
    def Initialize(self):
        pass

    def PostInitialize(self):  # Implemented in sub-classes
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
        self.subscribedTopics += 1

        # If user in options defined custom topics, use them and not the one choosen in the command
        if self.options and 'custom_topics' in self.options and len(self.options['custom_topics']) >= self.subscribedTopics:
            topic = self.options['custom_topics'][self.subscribedTopics-1]
            self.Log(Logger.LOG_INFO, 'Using custom topic defined in options')

        self.commandManager.mqttClient.AddNewTopic(topic, self)
        # Log the topic as debug if user wants
        if 'print_topics' in self.commandManager.config and self.commandManager.config['print_topics'] is True:
            self.Log(Logger.LOG_DEBUG, 'Subscribben to topic: ' + topic)

        return topic  # Return the topic cause upper function should now that topic may have been edited

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
