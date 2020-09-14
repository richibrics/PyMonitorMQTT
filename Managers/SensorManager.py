import sys
import inspect
import time
import Sensors
import Logger

CONFIG_SENSORS_KEY = 'sensors'

# Delay in second
update_rate = 20  # If not set in config


class SensorManager():
    commandManager = None
    sensors = []
    continue_sending = True  # Send loop condition

    def __init__(self, config, mqttClient, logger):
        self.config = config
        self.mqttClient = mqttClient
        self.update_rate = update_rate if 'update_rate' not in config else config[
            'update_rate']
        self.logger = logger

    def Start(self):
        # Start the send loop
        self.SendAllData()

    def InitializeSensors(self):
        self.LoadSensorsFromConfig()

    def PostInitializeSensors(self):
        for sensor in self.sensors:
            try:
                sensor.PostInitialize()
            except Exception as exc:
                self.Log(Logger.LOG_ERROR, sensor.name +
                         ': error during post-initialization: '+str(exc))
                self.UnloadSensor(sensor.name)

    def LoadSensorsFromConfig(self):
        if CONFIG_SENSORS_KEY in self.config:
            sensorsToAdd = self.config[CONFIG_SENSORS_KEY]
            for sensor in sensorsToAdd:
                self.LoadSensor(sensor)

    def LoadSensor(self, sensorString):
        name = sensorString
        options = None

        # If in the list I have a dict then I have some options for that command
        if type(sensorString) == dict:
            name = list(sensorString.keys())[0]
            options = sensorString[name]

        obj = self.GetSensorObjectByName(name)
        if obj:
            self.sensors.append(obj(self, options, self.logger))
            self.Log(Logger.LOG_INFO, name + ' sensor loaded')

    def UnloadSensor(self, name):
        obj = self.FindSensor(name)
        self.sensors.remove(obj)
        self.Log(Logger.LOG_WARNING, name + ' sensor unloaded')

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
        self.Log(Logger.LOG_ERROR, name + ' sensor not found')
        return None

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

                time.sleep(self.update_rate)
            else:
                time.sleep(1)

    def SetCommandManager(self, commandManager):
        self.commandManager = commandManager

    def Log(self, messageType, message):
        self.logger.Log(messageType, 'Sensor Manager', message)
