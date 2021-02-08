from Entity import Entity
import psutil
import json
from Logger import Logger, ExceptionTracker

supports_win_temperature = True
try:
    import wmi  # Only to get windows temperature
    openhardwaremonitor = wmi.WMI(namespace="root\\OpenHardwareMonitor")
except:
    supports_win_temperature = False


TOPIC = 'cpu/temperatures'


class CpuTemperaturesSensor(Entity):
    def Initialize(self):
        self.AddTopic(TOPIC)

    def Update(self):
        self.SetTopicValue(TOPIC, self.GetCpuTemperatures())

    def GetCpuTemperatures(self):
        os = self.GetOS()
        if(os == 'Windows'):
            return self.GetCpuTemperature_Win()
        # elif(Get_Operating_System() == 'macOS'):
        #    return Get_Temperatures_macOS() NOT SUPPORTED
        elif(os == 'Linux'):
            return self.GetCpuTemperature_Unix()
        else:
            raise Exception(
                'No temperature sensor available for this operating system')

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.FindEntity('Os')
        if os:
            os.Update()
            return os.GetTopicValue()

    def GetCpuTemperature_Unix(self):
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            for temp in temps['coretemp']:
                if 'Core' in temp.label:
                    return temp.current
        elif 'cpu_thermal' in temps:
            for temp in temps['cpu_thermal']:
                return temp.current
        else:
            self.Log(Logger.LOG_ERROR, "Can't get temperature for your system.")
            self.Log(Logger.LOG_ERROR,
                     "Open a Git Issue and show this: " + str(temps))
            self.Log(Logger.LOG_ERROR, "Thank you")
            raise Exception("No dict data")
        # Send the list as json
        raise Exception("No temperature data found")

    def GetCpuTemperature_Win(self):
        if supports_win_temperature:
            # Needs OpenHardwareMonitor interface for WMI
            sensors = openhardwaremonitor.Sensor()
            for sensor in sensors:
                if sensor.SensorType == u'Temperature' and not 'GPU' in sensor.Name:
                    return float(sensor.Value)
        raise Exception("No temperature data found")

    # def GetCpuTemperatures_macOS():
        #command = commands['macOS']['temperature'] + ' | grep \'temperature\''
        # print(command)
        # out = subprocess.Popen(command.split(),
        #                       stdout=subprocess.PIPE,
        #                       stderr=subprocess.STDOUT)
        #out, errors = out.communicate()
        # from out, I have to get the float with temperature
        #temperature = [re.findall("\d+\.\d+", str(out))]
        # print(temperature)
        # Send the list as json
        # return str(json.dumps(temperature))
