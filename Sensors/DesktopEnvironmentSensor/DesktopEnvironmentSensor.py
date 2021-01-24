import os
from Sensors.Sensor import *
from consts import *

TOPIC = 'desktop_environment'


class DesktopEnvironmentSensor(Sensor):
    def Initialize(self):
        self.AddTopic(TOPIC)

    def Update(self):
        self.SetTopicValue(TOPIC, self.GetDesktopEnvironment())

    # If value passed use it else get it from the system
    def GetDesktopEnvironment(self):

        de = os.environ.get('DESKTOP_SESSION')
        if de == None:
            de = "base"
       
        # If I have the value in the options, send that. otherwise try to get that                    
        return self.GetOption([CONTENTS_OPTION_KEY,"value"],de)
        
