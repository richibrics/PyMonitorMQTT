import Sensors
import Commands
from Configurator import Configurator as cf
import Managers
from MqttClient import MqttClient
import Logger
import multiprocessing
from consts import *


class Monitor():

    def __init__(self, config, globalConfig, commandManager, sensorManager, monitor_id=1):
        self.config = config
        self.globalConfig = globalConfig
        self.monitor_id = monitor_id
        self.commandManager = commandManager
        self.sensorManager = sensorManager
        # Some Sensors and Commands, after load, will return which sensor or command they need to run
        self.requirements = []
        self.loadedSensors = []  # To avoid reload for requirements, something is working
        self.loadedCommands = []  # To avoid reload for requirements, something is working
        self.Setup()

    def Setup(self):
        # Setip logger
        self.logger = Logger.Logger(self.globalConfig, self.monitor_id)
        self.Log(Logger.LOG_INFO, 'Starting')
        # Setup MQTT client
        self.mqttClient = MqttClient(self.config, self.logger)

        if CONFIG_SENSORS_KEY in self.config:
            self.LoadSensors(self.config[CONFIG_SENSORS_KEY])
        if CONFIG_COMMANDS_KEY in self.config:
            self.LoadCommands(self.config[CONFIG_COMMANDS_KEY])
        # While because some requirements may need other requirements themselves
        while(len(self.requirements)):
            self.Log(Logger.LOG_INFO, "Loading dependencies...")
            self.LoadRequirements()

        # Some need post-initialize configuration
        self.sensorManager.PostInitializeSensors()
        # Some need post-initialize configuration
        self.commandManager.PostInitializeCommands()

    def LoadSensors(self, sensorsToAdd, loadingRequirements=False):
        # From configs I read sensors list and I give the names to the sensors manager which will initialize them
        # and will keep trace of who is the mqtt_client and the logger of the sensor
        # self.sensorManager.PostInitializeSensors()
        if sensorsToAdd:
            for sensor in sensorsToAdd:
                # I load the sensor and if I need some requirements, I save them to the list
                # Additional check to not load double if I am loading requirements
                if not (loadingRequirements and sensor in self.loadedSensors):
                    settings = self.sensorManager.LoadSensor(
                        sensor, self.monitor_id, self.config, self.mqttClient, self.config['send_interval'], self.logger)
                    requirements = cf.GetOption(settings,SETTINGS_REQUIREMENTS_KEY)
                    if requirements:
                        self.requirements.append(requirements)
                    self.loadedSensors.append(sensor)

    def LoadCommands(self, commandsToAdd, loadingRequirements=False):
        # From configs I read commands list and I give the names to the commands manager which will initialize them
        # and will keep trace of who is the mqtt_client and the logger of the command
        if commandsToAdd:
            for command in commandsToAdd:
                # I load the command and if I need some requirements, I save them to the list
                # Additional check to not load double if I am loading requirements
                if not (loadingRequirements and command in self.loadedCommands):
                    settings = self.commandManager.LoadCommand(
                        command, self.monitor_id, self.config, self.mqttClient, self.logger)
                    requirements = cf.GetOption(settings,SETTINGS_REQUIREMENTS_KEY)
                    if requirements:
                        self.requirements.append(requirements)
                    self.loadedCommands.append(command)

    def LoadRequirements(self):
        # Here I load sensors and commands
        # I have a dict with {'sensors':[SENSORS],'commands':[COMMANDS]}
        # SENSORS and COMMANDS have the same format as the configutaration.yaml so I
        # tell to LoadSensor and LoadCommands what to load with the usual method
        for requirements in self.requirements:
            sensors = cf.GetOption(requirements,SETTINGS_REQUIREMENTS_SENSOR_KEY)
            commands = cf.GetOption(requirements,SETTINGS_REQUIREMENTS_COMMAND_KEY)
            if sensors:
                self.LoadSensors(
                    sensors, loadingRequirements=True)
            if commands:
                self.LoadCommands(
                    commands, loadingRequirements=True)
            self.requirements.remove(requirements)

    def Log(self, messageType, message):
        self.logger.Log(messageType, 'Main', message)
