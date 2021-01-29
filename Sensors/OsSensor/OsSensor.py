import platform
from Entity import Entity
#from consts import FIXED_VALUE_OS_MACOS

TOPIC = 'operating_system'


class OsSensor(Entity):
    def Initialize(self):
        self.AddTopic(TOPIC)

    def Update(self):
        self.SetTopicValue(TOPIC, self.GetOperatingSystem())

    def GetOperatingSystem(self):
        os = platform.system()
        if os == 'Darwin':  # It's macOS
            return self.consts.FIXED_VALUE_OS_MACOS
        return os
