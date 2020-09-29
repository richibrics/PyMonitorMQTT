import psutil
import math
from Sensors.Sensor import *

DOWNLOAD_TOPIC = 'bytes_recv'
UPLOAD_TOPIC = 'bytes_sent'

# Supports FORMATTED


class NetworkSensor(Sensor):
    def Initialize(self):

        self.AddTopic(DOWNLOAD_TOPIC)
        self.AddTopic(UPLOAD_TOPIC)

    def Update(self):
        self.SetTopicValue(DOWNLOAD_TOPIC, psutil.net_io_counters()[
                           1], ValueFormatter.TYPE_BYTE)
        self.SetTopicValue(UPLOAD_TOPIC, psutil.net_io_counters()[
                           0], ValueFormatter.TYPE_BYTE)
