from Entity import Entity
import subprocess

supports_win_brightness = True
try:
    import wmi  # Only to get windows brightness
    import pythoncom
except:
    supports_win_brightness = False


IN_TOPIC = 'brightness/set'  # Receive a set message
OUT_TOPIC = 'brightness/get'  # Send a message with the value


class BrightnessCommand(Entity):
    def Initialize(self):
        self.SubscribeToTopic(IN_TOPIC)
        self.AddTopic(OUT_TOPIC)
        self.stopCommand = False
        self.stopSensor = False
        self.stateOff = False

    def Callback(self, message):
        state = message.payload.decode("utf-8")
        if not self.stopCommand:

            if state == self.consts.ON_STATE and self.stateOff is not False:
                state = self.stateOff if self.stateOff is not None else 100

            if state == self.consts.OFF_STATE:
                self.stateOff = self.GetTopicValue(OUT_TOPIC)
                state = 1
            elif self.stateOff is not False:
                self.stateOff = False

            try:
                state = int(state)
            except:
                return

            # Well I can convert it to int
            self.SetBrightness(int(state))

            # Finally, tell the sensor to update and to send
            self.CallUpdate()
            self.SendOnlineState()
            self.lastSendingTime = None

    def Update(self):
        if not self.stopSensor:
            self.SetTopicValue(OUT_TOPIC, self.GetBrightness(),
                               self.ValueFormatter.TYPE_PERCENTAGE)

    def GetBrightness(self):
        os = self.GetOS()
        if(os == self.consts.FIXED_VALUE_OS_WINDOWS):
            return self.GetBrightness_Win()
        elif(os == self.consts.FIXED_VALUE_OS_MACOS):
            return self.GetBrightness_macOS()
        elif(os == self.consts.FIXED_VALUE_OS_LINUX):
            return self.GetBrightness_Linux()
        else:
            self.Log(self.Logger.LOG_WARNING,
                     'No brightness sensor available for this operating system')
            self.stopSensor = True

    def SetBrightness(self, value):
        # Value from 0 and 100
        os = self.GetOS()
        if(os == self.consts.FIXED_VALUE_OS_WINDOWS):
            return self.SetBrightness_Win(value)
        elif(os == self.consts.FIXED_VALUE_OS_MACOS):
            return self.SetBrightness_macOS(value)
        elif(os == self.consts.FIXED_VALUE_OS_LINUX):
            return self.SetBrightness_Linux(value)
        else:
            self.Log(self.Logger.LOG_WARNING,
                     'No brightness command available for this operating system')
            self.stopCommand = True

    def SetBrightness_macOS(self, value):
        value = value/100  # cause I need it from 0 to 1
        command = 'brightness ' + str(value)
        subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    def SetBrightness_Linux(self, value):
        command = 'xbacklight -set ' + str(value)
        subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    def SetBrightness_Win(self, value):
        if supports_win_brightness:
            pythoncom.CoInitialize()
            return wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(value, 0)
        else:
            raise Exception(
                'No WMI module installed')

    def GetBrightness_macOS(self):
        try:
            command = 'brightness -l'
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            stdout = process.communicate()[0]
            brightness = re.findall(
                'display 0: brightness.*$', str(stdout))[0][22:30]
            brightness = float(brightness)*100  # is between 0 and 1
            return brightness
        except:
            raise Exception(
                'You sure you installed Brightness from Homebrew ? (else try checking you PATH)')

    def GetBrightness_Linux(self):
        try:
            command = 'xbacklight'
            process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            stdout = process.communicate()[0]
            brightness = float(stdout)
            return brightness
        except:
            raise Exception(
                'You sure you installed Brightness from Homebrew ? (else try checking you PATH)')

    def GetBrightness_Win(self):
        if supports_win_brightness:
            return int(wmi.WMI(namespace='wmi').WmiMonitorBrightness()
                       [0].CurrentBrightness)
        else:
            raise Exception(
                'No WMI module installed')

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.FindEntity('Os')
        if os:
            os.Update()
            return os.GetTopicValue()

    def ManageDiscoveryData(self, discovery_data):
        for data in discovery_data:
            data['expire_after']=""

        self.SendOnlineState()

        discovery_data[0]['payload']['brightness_state_topic'] = self.SelectTopic(
            OUT_TOPIC)
        discovery_data[0]['payload']['state_topic'] = self.SelectTopic(
            self.STATE_TOPIC)
        discovery_data[0]['payload']['brightness_command_topic'] = self.SelectTopic(
            IN_TOPIC)
        discovery_data[0]['payload']['command_topic'] = self.SelectTopic(
            IN_TOPIC)
        discovery_data[0]['payload']['payload_on'] = self.consts.ON_STATE
        discovery_data[0]['payload']['payload_off'] = self.consts.OFF_STATE
        discovery_data[0]['payload']['brightness_scale'] = 100

        return discovery_data

    STATE_TOPIC = 'brightness/state'

    def SendOnlineState(self):
        if self.GetTopicValue(OUT_TOPIC) and int(self.GetTopicValue(OUT_TOPIC)) > 1:
            self.mqtt_client.SendTopicData(
                self.SelectTopic(self.STATE_TOPIC), self.consts.ON_STATE)
        else:
            self.mqtt_client.SendTopicData(
                self.SelectTopic(self.STATE_TOPIC), self.consts.OFF_STATE)
