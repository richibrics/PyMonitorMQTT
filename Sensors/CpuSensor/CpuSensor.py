import psutil
from Sensors.Sensor import Sensor


TOPIC = 'cpu_used_percentage'


class CpuSensor(Sensor):
    def Initialize(self):
        self.AddTopic(TOPIC)

    def Update(self):
        self.SetTopicValue(TOPIC, self.GetCpuPercentage())

    def GetCpuPercentage(self):
        return psutil.cpu_percent()
