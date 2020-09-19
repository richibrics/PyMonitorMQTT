from Sensors.Sensor import Sensor
from os import path
from ctypes import*

TOPIC_LEVEL = 'volume_level_get'
TOPIC_MUTE = 'volume_mute_get'

scriptFolder = str(path.dirname(path.realpath(__file__)))
#EXTERNAL_SOFTWARE_FILENAME = path.join(scriptFolder,'..','..','ExternalUtilities','FILE')

class VolumeSensor(Sensor):
    def Initialize(self):
        self.AddTopic(TOPIC_LEVEL)
        self.AddTopic(TOPIC_MUTE)

    def Update(self):
        self.GetSystemVolume()
        #self.SetTopicValue(TOPIC, self.GetSystemVolume())

    def GetSystemVolume(self):
        os = self.GetOS()
        raise Exception('No volume method coded') # for this Operating System')

    def GetWindowsVolume(self):
        pass


    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.FindSensor('Os')
        if os:
            os.Update()
            return os.GetTopicValue()

