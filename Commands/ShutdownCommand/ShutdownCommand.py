import subprocess
from Entity import Entity

TOPIC = 'shutdown_command'


commands = {
    'Windows': 'shutdown /s /t 0',
    'macOS': 'sudo shutdown -h now',
    'Linux': 'sudo shutdown -h now'
}


class ShutdownCommand(Entity):
    def Initialize(self):
        self.SubscribeToTopic(TOPIC)

    def Callback(self, message):
        try:
            command = commands[self.GetOS()]
            subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        except:
            raise Exception(
                'No shutdown command for this Operating System')

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.FindEntity('Os')
        if os:
            os.Update()
            return os.GetTopicValue()
