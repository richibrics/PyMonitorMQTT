import platform
from Sensors.Sensor import *


TOPIC = 'operating_system'


class OsSensor(Sensor):
    def Initialize(self):
        self.AddTopic(TOPIC)

    def Update(self):
        self.SetTopicValue(TOPIC, self.GetOperatingSystem())

    def GetOperatingSystem(self):
        os = platform.system()
        if os == 'Darwin':  # It's macOS
            return 'macOS'
        return os
