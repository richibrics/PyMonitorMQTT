import subprocess
from Entity import Entity
import Logger

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


class LockCommand(Entity):
    def Initialize(self):
        self.SubscribeToTopic(TOPIC)

    def Callback(self, message):
        os = self.GetOS()
        de=self.GetDE()
        if os in commands:
            if de in commands[os]:
                try:
                    command = commands[os][de]
                    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                except Exception as e:
                    raise Exception('Error during system lock: ' + str(e))
            else:
                raise Exception(
                    'No lock command for this Desktop Environment: ' + de)
        else:
            raise Exception(
                'No lock command for this Operating System: ' + os)

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.FindEntity('Os')
        if os:
            os.Update()
            return os.GetTopicValue()

    def GetDE(self):
        # Get OS from OsSensor and get temperature based on the os
        de = self.FindEntity(
            'DesktopEnvironment')
        if de:
            de.Update()
            return de.GetTopicValue()
