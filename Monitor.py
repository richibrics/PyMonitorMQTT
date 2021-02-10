from Configurator import Configurator as cf
from MqttClient import MqttClient
from Logger import Logger, ExceptionTracker
import multiprocessing
from consts import *


class Monitor():

    def __init__(self, config, globalConfig, entityManager, monitor_id=1):
        self.config = config
        self.globalConfig = globalConfig
        self.monitor_id = monitor_id
        self.entityManager = entityManager
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

        # HERE I TAKE THE SENSORS AND COMMANDS NAME FROM THE CONFIGURATION AND ASSIGN THE SUFFIX TO THE NAME TO LOAD THEM CORRECTLY. Add here the Custom part
        if CONFIG_SENSORS_KEY in self.config:
            self.LoadEntities(
                self.config[CONFIG_SENSORS_KEY], SENSOR_NAME_SUFFIX)
        if CONFIG_COMMANDS_KEY in self.config:
            self.LoadEntities(
                self.config[CONFIG_COMMANDS_KEY], COMMAND_NAME_SUFFIX)

        # While because some requirements may need other requirements themselves
        while(len(self.requirements)):
            self.Log(Logger.LOG_INFO, "Loading dependencies...")
            self.LoadRequirements()

        # Some need post-initialize configuration
        self.entityManager.PostInitializeEntities()
        # Some need post-initialize configuration
        # self.commandManager.PostInitializeCommands()

    def LoadEntities(self, entitiesToAdd, name_suffix, loadingRequirements=False):
        # From configs I read sensors list and I give the names to the sensors manager which will initialize them
        # and will keep trace of who is the mqtt_client and the logger of the sensor
        # self.entityManager.PostInitializeEntities()
        if entitiesToAdd:
            for entity in entitiesToAdd:
                # I load the sensor and if I need some requirements, I save them to the list
                # Additional check to not load double if I am loading requirements
                if not (loadingRequirements and entity in self.loadedEntities):
                    settings = self.entityManager.LoadEntity(name_suffix,
                                                              entity, self.monitor_id, self.config, self.mqttClient, self.config['send_interval'], self.logger)
                    requirements = cf.GetOption(
                        settings, SETTINGS_REQUIREMENTS_KEY)
                    if requirements:
                        self.requirements.append(requirements)
                    self.loadedEntities.append(entity)

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
                self.LoadEntities(sensors, SENSOR_NAME_SUFFIX, loadingRequirements=True)
            if commands:
                self.LoadEntities(commands, COMMAND_NAME_SUFFIX, loadingRequirements=True)
        
            self.requirements.remove(requirements)

    def Log(self, messageType, message):
        self.logger.Log(messageType, 'Main', message)
