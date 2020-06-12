from Sensors.Sensor import Sensor

supports_win_brightness = True
try:
    import wmi  # Only to get windows brightness
except:
    supports_win_brightness = False


TOPIC = 'brightness_get'


class BrightnessSensor(Sensor):
    def Initialize(self):
        self.AddTopic(TOPIC)

    def Update(self):
        self.SetTopicValue(TOPIC, self.GetBrightness())

    def GetBrightness(self):
        os = self.GetOS()
        if(os == 'Windows'):
            return self.GetBrightness_Win()
        else:
            raise Exception(
                'No brightness sensor available for this Operating System')

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.sensorManager.FindSensor('Os')
        if os:
            os.Update()
            return os.GetTopicValue()

    def GetBrightness_Win(self):
        if supports_win_brightness:
            return int(wmi.WMI(namespace='wmi').WmiMonitorBrightness()
                       [0].CurrentBrightness)
        else:
            raise Exception(
                'No WMI module installed')
