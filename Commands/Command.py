from consts import *


class Command():
    topic = ""

    def __init__(self, commandManager):  # Config is args
        self.commandManager = commandManager
        self.name = self.GetCommandName()
        self.Initialize()

    # Implemented in sub-classes
    def Initialize(self):
        pass

    def CallCallback(self, message):  # Safe method to run the Callback
        try:
            self.Callback(message)
        except Exception as exc:
            print('Error during', self.name, 'callback')
            print("Exception:", str(exc))
            self.commandManager.UnloadCommand(self.name)

    # Implemented in sub-classes
    def Callback(self, message):  # Run by the OnMessageEvent
        pass

    def SubscribeToTopic(self, topic):
        self.commandManager.mqttClient.AddNewTopic(topic, self)

    def GetTopic(self, last_part_of_topic):
        return TOPIC_FORMAT.format(self.commandManager.config['name'], last_part_of_topic)

    def GetClassName(self):
        # Command.SENSORFOLDER.SENSORCLASS
        return self.__class__.__name__

    def GetCommandName(self):
        # Only SENSORCLASS (without Command suffix)
        return self.GetClassName().split('.')[-1].split('Command')[0]
