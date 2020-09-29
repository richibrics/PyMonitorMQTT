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
        if 'values' in self.sensorManager.config:
            if 'DesktopEnvironment' in self.sensorManager.config['values']:
                return self.sensorManager.config['values']['DesktopEnvironment']

        de = os.environ.get('DESKTOP_SESSION')
        if de != None:
            return de
        else:
            return "base"
