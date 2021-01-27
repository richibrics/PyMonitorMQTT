import subprocess
import ctypes
import os as sys_os
from Sensors.Sensor import Sensor
from ctypes import *

TOPIC = 'turn_on_monitors_command'


class TurnOnMonitorsCommand(Sensor):
    def Initialize(self):
        self.SubscribeToTopic(self.FormatTopic(TOPIC))

    def Callback(self, message):
        os = self.GetOS()
        if os == 'Windows':
            ctypes.windll.user32.SendMessageA(0xFFFF, 0x0112, 0xF170, -1)  # Untested
        elif os == 'Linux':
            # Check if X11 or something else
            if sys_os.environ.get('DISPLAY'):
                command = 'xset dpms force on'
                subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            else:
                raise Exception(
                    'The Turn ON Monitors command is not available for this Linux Window System')

        else:
            raise Exception(
                'The Turn ON Monitors command is not available for this Operating System')

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.FindEntity('Os')
        if os:
            os.Update()
            return os.GetTopicValue()
