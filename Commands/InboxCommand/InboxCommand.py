from Sensors.Sensor import Sensor
import Logger

TOPIC = 'inbox_command'

# Great to be used with the custom topic and # wildcard to discover on which topic messages are received


class InboxCommand(Sensor):
    def Initialize(self):
        self.SubscribeToTopic(self.FormatTopic(TOPIC))

    def Callback(self, message):
        self.Log(Logger.LOG_INFO, 'Message received from topic: ' +
                 str(message.topic))
        self.Log(Logger.LOG_MESSAGE,
                 'Message received from topic: ' + str(message.payload))
