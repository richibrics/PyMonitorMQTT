from Sensors.Sensor import Sensor
import subprocess

supports_win_brightness = True
try:
    import wmi  # Only to get windows brightness
    import pythoncom
except:
    supports_win_brightness = False


TOPIC = 'brightness/set'


class BrightnessCommand(Sensor):
    def Initialize(self):
        self.SubscribeToTopic(self.FormatTopic(TOPIC))

    def Callback(self, message):
        self.SetBrightness(int(message.payload))

    def SetBrightness(self, value):
        # Value from 0 and 100
        os = self.GetOS()
        if(os == 'Windows'):
            return self.SetBrightness_Win(value)
        elif(os == 'macOS'):
            return self.SetBrightness_macOS(value)
        elif(os == 'Linux'):
            return self.SetBrightness_Linux(value)
        else:
            raise Exception(
                'No brightness command available for this Operating System')

    def SetBrightness_macOS(self, value):
        value = value/100  # cause I need it from 0 to 1
        command = 'brightness ' + str(value)
        subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    def SetBrightness_Linux(self, value):
        command = 'xbacklight -set ' + str(value)
        subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    def SetBrightness_Win(self, value):
        if supports_win_brightness:
            pythoncom.CoInitialize()
            return wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(value, 0)
        else:
            raise Exception(
                'No WMI module installed')

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.FindEntity('Os')
        if os:
            os.Update()
            return os.GetTopicValue()
