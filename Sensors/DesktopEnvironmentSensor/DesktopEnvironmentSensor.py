import os
from Sensors.Sensor import *


TOPIC = 'desktop_environment'


class DesktopEnvironmentSensor(Sensor):
    def Initialize(self):
        self.AddTopic(TOPIC)

    def Update(self):
        self.SetTopicValue(TOPIC, self.GetDesktopEnvironment())

    # If value passed use it else get it from the system
    def GetDesktopEnvironment(self):
        # If I have the value in the options, send that. otherwise try to get that
        if self.GetOption(CONTENTS_OPTION_KEY):
            if 'value' in self.GetOption(CONTENTS_OPTION_KEY):
                return self.GetOption(CONTENTS_OPTION_KEY)['value']

        de = os.environ.get('DESKTOP_SESSION')
        if de != None:
            return de
        else:
            return "base"
