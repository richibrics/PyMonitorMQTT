import platform
from Sensors.Sensor import *
from consts import FIXED_VALUE_OS_MACOS

TOPIC = 'operating_system'


class OsSensor(Sensor):
    def Initialize(self):
        self.AddTopic(TOPIC)

    def Update(self):
        self.SetTopicValue(TOPIC, self.GetOperatingSystem())

    def GetOperatingSystem(self):
        os = platform.system()
        if os == 'Darwin':  # It's macOS
            return FIXED_VALUE_OS_MACOS
        return os
