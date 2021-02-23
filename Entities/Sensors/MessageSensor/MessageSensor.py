import os
from Entities.Entity import Entity
import Schemas

TOPIC = 'message'
default_message = "default"

config_content_message_key = "message"

class MessageSensor(Entity):
    def Initialize(self):
        self.AddTopic(TOPIC)

    # I have also contents with message (required) in config
    def EntitySchema(self):
        schema = super().EntitySchema()
        schema = schema.extend({
            Schemas.Required(self.consts.CONTENTS_OPTION_KEY):  {
                Schemas.Required(config_content_message_key): str
            }
        })
        return schema

    def Update(self):
        message = self.GetOption([self.consts.CONTENTS_OPTION_KEY,config_content_message_key],default_message)
        self.SetTopicValue(TOPIC, message)
