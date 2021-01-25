import sys
import inspect
import time
import Sensors
import Logger

# Delay in second
update_rate = 20  # If not set in config


class SensorManager():
    # sensors is a list of dicts: [{sensor, mqtt_client, logger}]
    sensors = []
    commandManager = None
    continue_sending = True  # Stop loop condition

    def __init__(self, config):
        self.config = config
        self.logger = Logger.Logger(config)

    def Start(self):
        # Start the send loop
        self.SendAllData()

    def PostInitializeSensors(self):
        for sensor in self.sensors:
            try:
                sensor.PostInitialize()
            except Exception as exc:
                self.Log(Logger.LOG_ERROR, sensor.name +
                         ': error during post-initialization')
                self.Log(Logger.LOG_ERROR,
                         Logger.ExceptionTracker.TrackString(exc))
                self.UnloadSensor(sensor.name, sensor.GetMonitorID())

    # Here I receive the name of the sensor (or maybe also the options) and pass it to a function to get the object
    # which will be initialized and appended in the list of sensors
    # Here configs are specific for the monitor, it's not the same as this manager

    def LoadSensor(self, sensorString, monitor_id, config, mqtt_client, send_interval, logger):
        name = sensorString
        options = None

        # If in the list I have a dict then I have some options for that command
        if type(sensorString) == dict:
            name = list(sensorString.keys())[0]
            options = sensorString[name]

        obj = self.GetSensorObjectByName(name)
        if obj:
            try:
                objAlive = obj(monitor_id, config, mqtt_client,
                               send_interval, options, logger, self)
                self.sensors.append(objAlive)
                req = objAlive.LoadRequirements()
                self.Log(Logger.LOG_INFO, name +
                         ' sensor loaded', logger=logger)
                return req  # Return the requirements
            except Exception as exc:
                self.Log(Logger.LOG_ERROR, name +
                         ' sensor occured an error during loading: ' + str(exc), logger=logger)
                self.Log(Logger.LOG_ERROR, Logger.ExceptionTracker.TrackString(
                    exc), logger=logger)
        return None

    def UnloadSensor(self, name, monitor_id):
        obj = self.FindSensor(name, monitor_id)
        self.Log(Logger.LOG_WARNING, name +
                 ' sensor unloaded', logger=obj.GetLogger())
        self.sensors.remove(obj)

    def FindSensor(self, name, monitor_id):
        # Return the sensor object present in sensors list: to get sensor value from another sensor for example
        for sensor in self.ActiveSensors():
            # If it's an object->obj.name, if a class must use the .__dict__ for the name
            if name == sensor.name and monitor_id == sensor.GetMonitorID():
                return sensor
        return None

    def ActiveSensors(self):
        return self.sensors

    def GetSensorObjectByName(self, name):
        sensorList = self.GetSensorObjectsList()
        for sensor in sensorList:
            if name == self.GetSensorName(sensor):
                return sensor
        self.Log(Logger.LOG_ERROR, str(name) + ' sensor not found - check the module import line is added'
                                               ' to Sensors/__init__.py')
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

    # Also discovery data every X second
    def SendAllData(self):
        while self.continue_sending:
            for sensor in self.ActiveSensors():
                if sensor.GetMqttClient().connected:
                    if sensor.ShouldSendMessage():
                        sensor.CallUpdate()
                        sensor.SendData()
                        # Save this time as time when last message is sent
                        sensor.SaveTimeMessageSent()            
                    if sensor.ShouldSendDiscoveryConfig():
                        sensor.PublishDiscoveryData()
                        sensor.SaveTimeDiscoverySent()
            time.sleep(1)  # Wait a second and recheck if someone has to send
            

    def SetCommandManager(self, commandManager):
        self.commandManager = commandManager

    def Log(self, messageType, message, logger=None):
        if logger is None:
            logger = self.logger
        logger.Log(messageType, 'Sensor Manager', message)
