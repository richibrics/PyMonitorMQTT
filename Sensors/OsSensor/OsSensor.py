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

    def ManageDiscoveryData(self, discovery_data):
        # Setup icons if I have a dict of OS in the settings
        icons = discovery_data[0]['payload']['icon']
        if (type(icons)==dict):
            os = self.GetTopicValue(self.GetFirstTopic())
            if os in icons:
                discovery_data[0]['payload']['icon'] = icons[os]
            else:
                discovery_data[0]['payload']['icon'] = "mdi:flask"
        return discovery_data