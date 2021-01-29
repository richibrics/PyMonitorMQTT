import Sensors
import Commands
from Configurator import Configurator as cf
from MqttClient import MqttClient
from Logger import Logger, ExceptionTracker
import multiprocessing
from consts import *


class Monitor():

    def __init__(self, config, globalConfig, valueFormatter, monitor_id=1):
        self.config = config
        self.globalConfig = globalConfig
        self.monitor_id = monitor_id
        self.ValueFormatter = valueFormatter
        # Some Sensors and Commands, after load, will return which sensor or command they need to run
        self.requirements = []
        self.loadedEntities = []  # To avoid reload for requirements, something is working
        self.Setup()

    def Setup(self):
        # Setup logger
        self.logger = Logger(self.globalConfig, self.monitor_id)
        self.Log(Logger.LOG_INFO, 'Starting')
        # Setup MQTT client
        self.mqttClient = MqttClient(self.config, self.logger)

        if CONFIG_SENSORS_KEY in self.config:
            self.LoadEntities(
                self.config[CONFIG_SENSORS_KEY], SENSOR_NAME_SUFFIX, SENSORS_MODULE_NAME)
        if CONFIG_COMMANDS_KEY in self.config:
            self.LoadEntities(
                self.config[CONFIG_COMMANDS_KEY], COMMAND_NAME_SUFFIX, COMMAND_MODULE_NAME)
        # While because some requirements may need other requirements themselves
        while(len(self.requirements)):
            self.Log(Logger.LOG_INFO, "Loading dependencies...")
            self.LoadRequirements()

        # Some need post-initialize configuration
        self.ValueFormatter.PostInitializeSensors()
        # Some need post-initialize configuration
        # self.commandManager.PostInitializeCommands()

    def LoadEntities(self, entitiesToAdd, name_suffix, module_name, loadingRequirements=False):
        # From configs I read sensors list and I give the names to the sensors manager which will initialize them
        # and will keep trace of who is the mqtt_client and the logger of the sensor
        # self.ValueFormatter.PostInitializeSensors()
        if entitiesToAdd:
            for entity in entitiesToAdd:
                # I load the sensor and if I need some requirements, I save them to the list
                # Additional check to not load double if I am loading requirements
                if not (loadingRequirements and entity in self.loadedEntities):
                    settings = self.ValueFormatter.LoadEntity(name_suffix, module_name,
                                                              entity, self.monitor_id, self.config, self.mqttClient, self.config['send_interval'], self.logger)
                    requirements = cf.GetOption(
                        settings, SETTINGS_REQUIREMENTS_KEY)
                    if requirements:
                        self.requirements.append(requirements)
                    self.loadedEntities.append(entity)

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
                    requirements = cf.GetOption(
                        settings, SETTINGS_REQUIREMENTS_KEY)
                    if requirements:
                        self.requirements.append(requirements)
                    self.loadedCommands.append(command)

    def LoadRequirements(self):
        # Here I load sensors and commands
        # I have a dict with {'sensors':[SENSORS],'commands':[COMMANDS]}
        # SENSORS and COMMANDS have the same format as the configutaration.yaml so I
        # tell to LoadSensor and LoadCommands what to load with the usual method
        for requirements in self.requirements:
            sensors = cf.GetOption(
                requirements, SETTINGS_REQUIREMENTS_SENSOR_KEY)
            commands = cf.GetOption(
                requirements, SETTINGS_REQUIREMENTS_COMMAND_KEY)
            if sensors:
                self.LoadSensors(
                    sensors, loadingRequirements=True)
            if commands:
                self.LoadCommands(
                    commands, loadingRequirements=True)
            self.requirements.remove(requirements)

    def Log(self, messageType, message):
        self.logger.Log(messageType, 'Main', message)
