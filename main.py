import os
import yaml
import Sensors
import Commands
import Managers
from MqttClient import MqttClient
import Logger

sensorManager = None
config = None
config_filename = 'configuration.yaml'

scriptFolder = str(os.path.dirname(os.path.realpath(__file__)))


def LoadYAML():
    global config
    with open(os.path.join(scriptFolder, config_filename)) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)


if __name__ == "__main__":
    LoadYAML()
    logger = Logger.Logger()
    logger.Log(Logger.LOG_INFO, 'Main', 'Starting')
    mqttClient = MqttClient(config, logger)
    commandManager = Managers.CommandManager(config, mqttClient, logger)
    sensorManager = Managers.SensorManager(config, mqttClient, logger)
    commandManager.SetSensorManager(sensorManager)
    sensorManager.SetCommandManager(commandManager)
    # All configurations must go above
    sensorManager.Start()  # Start the loop
