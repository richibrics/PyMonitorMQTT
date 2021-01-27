import subprocess
import os as sys_os
from Sensors.Sensor import Sensor

TOPIC = 'sleep_command'

commands = {
    'Windows': 'rundll32.exe powrprof.dll,SetSuspendState 0,1,0',
    'Linux_X11': 'xset dpms force standby'
}


class SleepCommand(Sensor):
    def Initialize(self):
        self.SubscribeToTopic(self.FormatTopic(TOPIC))

    def Callback(self, message):
        try:
            prefix = ''
            os_type = self.GetOS()

            # Additional linux checking to find Window Manager
            # TODO: Update TurnOffMonitors, TurnOnMonitors, ShutdownCommand, LockCommand to use prefix lookup below
            if os_type == 'Linux':
                # Check running X11
                if sys_os.environ.get('DISPLAY'):
                    prefix = '_X11'

            lookup_key = os_type + prefix
            command = commands[lookup_key]
            subprocess.Popen(command.split(), stdout=subprocess.PIPE)

        except:
            raise Exception(
                'No Sleep command for this Operating System')

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.FindEntity('Os')
        if os:
            os.Update()
            return os.GetTopicValue()
