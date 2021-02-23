import os
from Entities.Entity import Entity
import Schemas

TOPIC = 'desktop_environment'

CONTENTS_VALUE_OPTION_KEY = "value"

class DesktopEnvironmentSensor(Entity):
    def Initialize(self):
        self.AddTopic(TOPIC)

    # I have also contents with value (optional) in config
    def EntitySchema(self):
        schema = super().EntitySchema()
        schema = schema.extend({
            Schemas.Optional(self.consts.CONTENTS_OPTION_KEY):  {
                Schemas.Optional(CONTENTS_VALUE_OPTION_KEY): str
            }
        })
        return schema

    def Update(self):
        self.SetTopicValue(TOPIC, self.GetDesktopEnvironment())

    # If value passed use it else get it from the system
    def GetDesktopEnvironment(self):

        de = os.environ.get('DESKTOP_SESSION')
        if de == None:
            de = "base"
       
        # If I have the value in the options, send that. otherwise try to get that                    
        return self.GetOption([self.consts.CONTENTS_OPTION_KEY,CONTENTS_VALUE_OPTION_KEY],de)
