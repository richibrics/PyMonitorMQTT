import psutil
import math
from Entities.Entity import Entity
from ValueFormatter import ValueFormatter

DOWNLOAD_TOPIC = 'network/bytes_recv'
UPLOAD_TOPIC = 'network/bytes_sent'

# Supports FORMATTED

SIZE_OPTION_KEY = "size"

class NetworkSensor(Entity):
    def Initialize(self):

        self.AddTopic(DOWNLOAD_TOPIC)
        self.AddTopic(UPLOAD_TOPIC)

    def Update(self):
        self.SetTopicValue(DOWNLOAD_TOPIC, psutil.net_io_counters()[
                           1], self.ValueFormatter.TYPE_BYTE)
        self.SetTopicValue(UPLOAD_TOPIC, psutil.net_io_counters()[
                           0], self.ValueFormatter.TYPE_BYTE)

# Example in configuration:
#
#      - Network:
#          value_format:
#            size: MB // SIZE_....BYTE constant