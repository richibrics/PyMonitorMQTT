import sys
import inspect
import time
import Sensors

CONFIG_SENSORS_KEY = 'sensors'

# Delay in second
message_send_loop_delay = 20
not_connected_loop_delay = 1


class SensorManager():
    commandManager = None
    sensors = []
    continue_sending = True  # Send loop condition

    def __init__(self, config, mqttClient):
        self.config = config
        self.mqttClient = mqttClient
        self.LoadSensorsFromConfig()

    def Start(self):
        # Start the send loop
        self.SendAllData()

    def LoadSensorsFromConfig(self):
        if CONFIG_SENSORS_KEY in self.config:
            sensorsToAdd = self.config[CONFIG_SENSORS_KEY]
            for sensor in sensorsToAdd:
                self.LoadSensor(sensor)

    def LoadSensor(self, name):
        obj = self.GetSensorObjectByName(name)
        self.sensors.append(obj(self))
        print(name, 'sensor loaded')

    def UnloadSensor(self, name):
        obj = self.FindSensor(name)
        self.sensors.remove(obj)
        print(name, 'sensor unloaded')

    def FindSensor(self, name):
        # Return the sensor object present in sensors list: to get sensor value from another sensor for example
        for sensor in self.ActiveSensors():
            if name == sensor.name:  # If it's an object->obj.name, if a class must use the .__dict__ for the name
                return sensor
        return None

    def ActiveSensors(self):
        return self.sensors

    def GetSensorObjectByName(self, name):
        sensorList = self.GetSensorObjectsList()
        for sensor in sensorList:
            if name == self.GetSensorName(sensor):
                return sensor
        print(name, 'sensor not found')
        exit(1)

    def GetSensorObjectsList(self):
        classes = []
        for name, obj in inspect.getmembers(sys.modules['Sensors']):
            if inspect.isclass(obj):
                # Don't add Sensor parent class to the list
                if('.Sensor' not in self.GetClassName(obj)):
                    classes.append(obj)
        return classes

    def UpdateSensors(self):
        for sensor in self.sensors:
            sensor.CallUpdate()

    def SendSensorsData(self):
        for sensor in self.sensors:
            sensor.SendData()

    def GetClassName(self, sensor_class):
        # Sensor.SENSORFOLDER.SENSORCLASS
        return sensor_class.__dict__['__module__']

    def GetSensorName(self, sensor_class):
        # Only SENSORCLASS (without Sensor suffix)
        return self.GetClassName(sensor_class).split('.')[-1].split('Sensor')[0]

    def SendAllData(self):
        while self.continue_sending:
            if self.mqttClient.connected:
                # Update sensors and send data
                self.UpdateSensors()
                self.SendSensorsData()

                time.sleep(message_send_loop_delay)
            else:
                time.sleep(not_connected_loop_delay)

    def SetCommandManager(self, commandManager):
        self.commandManager = commandManager
