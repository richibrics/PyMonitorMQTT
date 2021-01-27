import subprocess
from Sensors.Sensor import Sensor

TOPIC = 'reboot_command'

commands = {
    'Windows': 'shutdown /r',
    'macOS': 'sudo reboot',
    'Linux': 'sudo reboot'
}


class RebootCommand(Sensor):
    def Initialize(self):
        self.SubscribeToTopic(self.FormatTopic(TOPIC))

    def Callback(self, message):
        try:
            command = commands[self.GetOS()]
            subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        except:
            raise Exception(
                'No reboot command for this Operating System')

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.FindEntity('Os')
        if os:
            os.Update()
            return os.GetTopicValue()
