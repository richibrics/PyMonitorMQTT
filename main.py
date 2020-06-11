import os
import time
import datetime
import yaml
import argparse
import Sensors
import Commands
import Managers
from MqttClient import MqttClient

sensorManager = None
config = None
config_filename = 'configuration.yaml'

scriptFolder = str(os.path.dirname(os.path.realpath(__file__)))


def Main():
    LoadYAML()
    mqttClient = MqttClient(config)
    commandManager = Managers.CommandManager(config, mqttClient)
    sensorManager = Managers.SensorManager(config, mqttClient)
    commandManager.SetSensorManager(sensorManager)
    sensorManager.SetCommandManager(commandManager)
    # All configurations must go above
    sensorManager.Start()  # Start the loop


def LoadYAML():
    global config
    with open(os.path.join(scriptFolder, config_filename)) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)


Main()
