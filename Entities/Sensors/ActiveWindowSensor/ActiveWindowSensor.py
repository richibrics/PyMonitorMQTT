from Entities.Entity import Entity

# Linux dep
try:
    import os, re, sys
    from subprocess import PIPE, Popen
    linux_support=True
except:
    linux_support=False


# Windows dep
try:
    from win32gui import GetWindowText, GetForegroundWindow
    windows_support=True
except:
    windows_support=False


TOPIC = 'active_window'


class ActiveWindowSensor(Entity):
    def Initialize(self):
        self.AddTopic(TOPIC)

    def PostInitialize(self):
        self.os = self.GetOS()

    def Update(self):
        self.SetTopicValue(TOPIC, str(self.GetActiveWindow()))


    def GetActiveWindow(self):
        if self.os == self.consts.FIXED_VALUE_OS_LINUX:
            if linux_support:
                return self.GetActiveWindow_Linux()
            else:
                raise Exception("Unsatisfied dependencies for this entity")
        elif self.os == self.consts.FIXED_VALUE_OS_WINDOWS:
            if windows_support:
                return self.GetActiveWindow_Windows()
            else:
                raise Exception("Unsatisfied dependencies for this entity")
        else:
            raise Exception(
                'Entity not available for this operating system')

    def GetActiveWindow_Windows(self):
        return GetWindowText(GetForegroundWindow())

    def GetActiveWindow_Linux(self):
        root = Popen( ['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout = PIPE )
        stdout, stderr = root.communicate()

        m = re.search( b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout )

        if m is not None:
            window_id = m.group( 1 )
            window = Popen( ['xprop', '-id', window_id, 'WM_NAME'], stdout = PIPE )
            stdout, stderr = window.communicate()

            match = re.match( b'WM_NAME\(\w+\) = (?P<name>.+)$', stdout )
            if match is not None:
                return match.group( 'name' ).decode( 'UTF-8' ).strip( '"' )

        return 'Inactive'

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.FindEntity('Os')
        if os:
            os.Update()
            return os.GetTopicValue()
