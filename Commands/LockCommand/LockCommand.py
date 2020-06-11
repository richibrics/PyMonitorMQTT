import subprocess
from Commands.Command import Command

TOPIC = 'lock_command'

commands = {
    'Windows': {
        'base': 'rundll32.exe user32.dll,LockWorkStation'
    },
    'macOS': {
        'base': 'pmset displaysleepnow'
    },
    'Linux': {
        'gnome': 'gnome-screensaver-command -l',
        'cinnamon': 'cinnamon-screensaver-command -a',
        'i3': 'i3lock'
    }
}


class LockCommand(Command):
    def Initialize(self):
        self.SubscribeToTopic(self.GetTopic(TOPIC))

    def Callback(self, message):
        try:
            command = commands[self.GetOS()][self.GetDE()]
            subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        except:
            raise Exception(
                'No Lock command for this Desktop Environment/Operating System')

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        if(self.commandManager.sensorManager):
            os = self.commandManager.sensorManager.FindSensor('Os')
            if os:
                os.Update()
                return os.GetTopicValue()
        else:
            print('SensorManager not set in the CommandManager!')

    def GetDE(self):
        # Get OS from OsSensor and get temperature based on the os
        if(self.commandManager.sensorManager):
            de = self.commandManager.sensorManager.FindSensor(
                'DesktopEnvironment')
            if de:
                de.Update()
                return de.GetTopicValue()
        else:
            print('SensorManager not set in the CommandManager!')
