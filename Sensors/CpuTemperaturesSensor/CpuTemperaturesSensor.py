from Sensors.Sensor import *
import psutil
import json

supports_win_temperature = True
try:
    import wmi  # Only to get windows temperature
    openhardwaremonitor = wmi.WMI(namespace="root\\OpenHardwareMonitor")
except:
    supports_win_temperature = False


TOPIC = 'cpu/temperatures'


class CpuTemperaturesSensor(Sensor):
    def Initialize(self):
        self.AddTopic(TOPIC)

    def Update(self):
        self.SetTopicValue(TOPIC, self.GetCpuTemperatures())

    def GetCpuTemperatures(self):
        os = self.GetOS()
        if(os == 'Windows'):
            return self.GetCpuTemperatures_Win()
        # elif(Get_Operating_System() == 'macOS'):
        #    return Get_Temperatures_macOS() NOT SUPPORTED
        elif(os == 'Linux'):
            return self.GetCpuTemperatures_Unix()
        else:
            raise Exception(
                'No temperature sensor available for this operating system')

    def GetOS(self):
        # Get OS from OsSensor and get temperature based on the os
        os = self.FindSensor('Os')
        if os:
            os.Update()
            return os.GetTopicValue()

    def GetCpuTemperatures_Unix(self):
        cpu_temps = []
        temps = psutil.sensors_temperatures()['coretemp']
        for temp in temps:
            if 'Core' in temp.label:
                cpu_temps.append(temp.current)
        # Send the list as json
        return str(json.dumps(cpu_temps))

    def GetCpuTemperatures_Win(self):
        if supports_win_temperature:
            # Needs OpenHardwareMonitor interface for WMI
            sensors = openhardwaremonitor.Sensor()
            cpu_temps = []
            for sensor in sensors:
                if sensor.SensorType == u'Temperature' and not 'GPU' in sensor.Name:
                    cpu_temps += [float(sensor.Value)]
            cpu_temps.pop()  # Cause last temp is the highest value (summary)
            # Send the list as json
            return str(json.dumps(cpu_temps))
        return 'None'

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
