import os
from Entities.Entity import Entity
from consts import *
from Configurator import Configurator as cf

TOPIC = 'message'
default_message = "default"

config_content_message_key = "message"

class MessageSensor(Entity):
    def Initialize(self):
        self.AddTopic(TOPIC)

    def Update(self):
        message = cf.GetOption(self.entityConfigs,[CONTENTS_OPTION_KEY,config_content_message_key],default_message)
        self.SetTopicValue(TOPIC, message)
