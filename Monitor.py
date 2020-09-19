import Sensors
import Commands
import Managers
from MqttClient import MqttClient
import Logger
import multiprocessing
from consts import *


class Monitor():

    def __init__(self, config, commandManager, sensorManager, monitor_id=1):
        self.config = config
        self.monitor_id = monitor_id
        self.commandManager = commandManager
        self.sensorManager = sensorManager
        self.Setup()

    def Setup(self):
        # Setip logger
        self.logger = Logger.Logger(self.monitor_id)
        self.Log(Logger.LOG_INFO, 'Starting')
        # Setup MQTT client
        self.mqttClient = MqttClient(self.config, self.logger)

        self.LoadSensors()
        self.LoadCommands()

    def LoadSensors(self):
        # From configs I read sensors list and I give the names to the sensors manager which will initialize them
        # and will keep trace of who is the mqtt_client and the logger of the sensor
        # self.sensorManager.PostInitializeSensors()
        if CONFIG_SENSORS_KEY in self.config:
            sensorsToAdd = self.config[CONFIG_SENSORS_KEY]
            for sensor in sensorsToAdd:
                self.sensorManager.LoadSensor(
                    sensor, self.monitor_id, self.config, self.mqttClient, self.config['send_interval'], self.logger)


    def LoadCommands(self):
        # From configs I read commands list and I give the names to the commands manager which will initialize them
        # and will keep trace of who is the mqtt_client and the logger of the command
        if CONFIG_COMMANDS_KEY in self.config:
            commandsToAdd = self.config[CONFIG_COMMANDS_KEY]
            for command in commandsToAdd:
                self.commandManager.LoadCommand(
                    command, self.monitor_id, self.config, self.mqttClient, self.logger)

        # Some need post-initialize configuration
        self.commandManager.PostInitializeCommands()
        # All configurations must go above


    def Log(self, messageType, message):
        self.logger.Log(messageType, 'Main', message)
