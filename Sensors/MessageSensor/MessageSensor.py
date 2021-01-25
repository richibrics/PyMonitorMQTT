import os
from Sensors.Sensor import *
from consts import *
from Configurator import Configurator as cf

TOPIC = 'message'
default_message = "default"

config_content_message_key = "message"

class MessageSensor(Sensor):
    def Initialize(self):
        self.AddTopic(TOPIC)

    def Update(self):
        message = cf.GetOption(self.sensorConfigs,[CONTENTS_OPTION_KEY,config_content_message_key],default_message)
        self.SetTopicValue(TOPIC, message)
