from Sensors.Sensor import Sensor
import subprocess
import re

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
        elif(os == 'macOS'):
            return self.GetBrightness_macOS()
        else:
            raise Exception(
                'No brightness sensor available for this operating system')

    def GetBrightness_macOS(self):
        try:
            command = 'brightness -l'
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            stdout = process.communicate()[0]
            brightness = re.findall(
                'display 0: brightness.*$', str(stdout))[0][22:30]
            brightness = float(brightness)*100  # is between 0 and 1
            return brightness
        except:
            raise Exception(
                'You sure you installed Brightness from Homebrew ? (else try checking you PATH)')

    def GetBrightness_Win(self):
        if supports_win_brightness:
            return int(wmi.WMI(namespace='wmi').WmiMonitorBrightness()
                       [0].CurrentBrightness)
        else:
            raise Exception(
                'No WMI module installed')

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.sensorManager.FindSensor('Os')
        if os:
            os.Update()
            return os.GetTopicValue()
