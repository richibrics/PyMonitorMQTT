import os
import yaml
import time
import Logger
import Managers
from Monitor import Monitor

config = None
config_filename = 'configuration.yaml'

scriptFolder = str(os.path.dirname(os.path.realpath(__file__)))


def LoadYAML():
    global config
    with open(os.path.join(scriptFolder, config_filename)) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)


def SetupMonitors():

    # Setup managers
    commandManager = Managers.CommandManager(
        config)
    sensorManager = Managers.SensorManager(
        config)
    # Link them
    commandManager.SetSensorManager(sensorManager)
    sensorManager.SetCommandManager(commandManager)

    # If I have not a list of monitors, I setup only a monitor
    if('monitors' not in config):
        monitor = Monitor(config, config, commandManager, sensorManager)
    else:  # More Monitors
        # Now setup monitors
        monitor_id = 0
        for monitor_config in config['monitors']:
            monitor_id += 1
            monitor = Monitor(monitor_config, config, commandManager,
                              sensorManager, monitor_id)

    # Start sensors loop
    sensorManager.Start()


if __name__ == "__main__":
    try:
        LoadYAML()
        SetupMonitors()
    except Exception as exc:  # Main try except to give information about exception management
        logger = Logger.Logger(config)
        logger.Log(Logger.LOG_ERROR, 'Main',
                   Logger.ExceptionTracker.TrackString(exc))
        logger.Log(Logger.LOG_ERROR, 'Main',
                   'Try to check your configuration.yaml')
        logger.Log(Logger.LOG_ERROR, 'Main',
                   "If problem persists, check issues (or open a new one) at 'https://github.com/richibrics/PyMonitorMQTT'")
        exit(1)
