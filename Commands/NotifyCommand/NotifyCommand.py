from Commands.Command import Command
import Logger

supports_win = True
try:
    import win10toast  # Only to get windows temperature
except:
    supports_win = False


supports_unix = True
try:
    import wmi  # Only to get windows temperature
except:
    supports_unix = False


TOPIC = 'notify'


class NotifyCommand(Command):
    def Initialize(self):
        self.SubscribeToTopic(self.GetTopic(TOPIC))

    # I need it here cause I have to check the right import for my OS (and I may not know the OS in Init function)
    def PostInitialize(self):
        os = self.GetOS()
        if os == 'Windows':
            if not supports_win:
                raise Exception(
                    'Notify not available, have you installed \'win10toast\' on pip ?')
        else:
            if not supports_unix:
                raise Exception(
                    'Notify not available, have you installed \'notify2\' on pip ?')

    def Callback(self, message):
        # TO DO
        pass

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        if(self.commandManager.sensorManager):
            os = self.commandManager.sensorManager.FindSensor('Os')
            if os:
                os.Update()
                return os.GetTopicValue()
        else:
            raise UserWarning('SensorManager not set in the CommandManager!')
