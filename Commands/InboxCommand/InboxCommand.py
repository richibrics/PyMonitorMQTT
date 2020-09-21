from Commands.Command import Command
import Logger

TOPIC = 'inbox_command'

# Great to be used with the custom topic and # wildcard to discover on which topic messages are received


class InboxCommand(Command):
    def Initialize(self):
        self.SubscribeToTopic(self.GetTopic(TOPIC))

    def Callback(self, message):
        self.Log(Logger.LOG_INFO, 'Message received from topic: ' +
                 str(message.topic))
        self.Log(Logger.LOG_MESSAGE,
                 'Message received from topic: ' + str(message.payload))
