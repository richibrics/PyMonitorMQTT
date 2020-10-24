import subprocess
import ctypes
from Commands.Command import Command
from ctypes import *

TOPIC = 'turn_off_monitors_command'

class TurnOffMonitorsCommand(Command):
    def Initialize(self):
        self.SubscribeToTopic(self.GetTopic(TOPIC))

    def Callback(self, message):
        os = self.GetOS()
        if(os == 'Windows'):
            ctypes.windll.user32.SendMessageA(0xFFFF, 0x0112, 0xF170, 2)
        else:
            raise Exception(
                'The Turn Off Monitors command is not available for this Operating System')

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.FindSensor('Os')
        if os:
            os.Update()
            return os.GetTopicValue()
