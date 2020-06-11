import psutil
from Sensors.Sensor import Sensor


TOPIC_RAM_PERCENTAGE = 'ram_used_percentage'


class RamSensor(Sensor):
    def Initialize(self):
        self.AddTopic(TOPIC_RAM_PERCENTAGE)

    def Update(self):
        self.SetTopicValue(TOPIC_RAM_PERCENTAGE, self.GetSystemRam())

    def GetSystemRam(self):
        return psutil.virtual_memory()[2]
