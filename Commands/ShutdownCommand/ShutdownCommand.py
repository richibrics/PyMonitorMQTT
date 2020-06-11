import subprocess
from Commands.Command import Command

TOPIC = 'shutdown_command'


commands = {
    'Windows': 'shutdown /s',
    'macOS': 'sudo shutdown -h now',
    'Linux': 'sudo shutdown -h now'
}


class ShutdownCommand(Command):
    def Initialize(self):
        self.SubscribeToTopic(self.GetTopic(TOPIC))

    def Callback(self, message):
        try:
            command = commands[self.GetOS()]
            subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        except:
            raise Exception(
                'No shutdown command for this Operating System')

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        if(self.commandManager.sensorManager):
            os = self.commandManager.sensorManager.FindSensor('Os')
            if os:
                os.Update()
                return os.GetTopicValue()
        else:
            print('SensorManager not set in the CommandManager!')
