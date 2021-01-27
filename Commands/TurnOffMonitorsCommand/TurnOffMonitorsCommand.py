import subprocess
import ctypes
import os as sys_os
from Sensors.Sensor import Sensor
from ctypes import *

TOPIC = 'turn_off_monitors_command'


class TurnOffMonitorsCommand(Sensor):
    def Initialize(self):
        self.SubscribeToTopic(self.FormatTopic(TOPIC))

    def Callback(self, message):
        os = self.GetOS()
        if os == 'Windows':
            ctypes.windll.user32.SendMessageA(0xFFFF, 0x0112, 0xF170, 2)
        elif os == 'Linux':
            # Check if X11 or something else
            if sys_os.environ.get('DISPLAY'):
                command = 'xset dpms force off'
                subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            else:
                raise Exception(
                    'The Turn Off Monitors command is not available for this Linux Window System')

        else:
            raise Exception(
                'The Turn Off Monitors command is not available for this Operating System')

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.FindEntity('Os')
        if os:
            os.Update()
            return os.GetTopicValue()
