import os
import yaml
import time
from Logger import Logger, ExceptionTracker
from EntityManager import EntityManager 
from ClassManager import ClassManager # To list entities in help
import consts
import sys
from Monitor import Monitor
from schemas import ROOT_SCHEMA

config = None
config_filename = 'configuration.yaml'

scriptFolder = str(os.path.dirname(os.path.realpath(__file__)))


def LoadYAML():
    global config
    with open(os.path.join(scriptFolder, config_filename)) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    config = ROOT_SCHEMA(config) # Here I validate che config schema (not for entities)


def SetupMonitors():
    # Setup manager
    entityManager = EntityManager(
        config)

    # If I have not a list of monitors, I setup only a monitor
    if (consts.CONFIG_MONITORS_KEY not in config):
        monitor = Monitor(config, config, entityManager)
    else:  # More Monitors
        # Now setup monitors
        monitor_id = 0
        for monitor_config in config[consts.CONFIG_MONITORS_KEY]:
            monitor_id += 1
            monitor = Monitor(monitor_config, config,
                              entityManager, monitor_id)

    # Start sensors loop
    entityManager.Start()


def OutputAvailableEntities():
    sensors = []
    commands = []
    classManager=ClassManager(None) # Loads the entities files

    for entityFilename in classManager.modulesFilename:
        entityName = classManager.ModuleNameFromPath(entityFilename)
        if consts.SENSOR_NAME_SUFFIX in entityName:
            sensors.append(entityName.split(consts.SENSOR_NAME_SUFFIX)[0])
        elif consts.COMMAND_NAME_SUFFIX in entityName:
            commands.append(entityName.split(consts.COMMAND_NAME_SUFFIX)[0])

    sensors.sort()
    commands.sort()
    
    if len(sensors) == 0:
        raise("Can't load any sensor")
    else:
        print("Sensors:")
        for sensor in sensors:
            print("    -",sensor)

    if len(commands) == 0:
        raise("Can't load any command")
    else:
        print("Commands:")
        for command in commands:
            print("    -",command)


if __name__ == "__main__":
    try:
        # Do we have a config file?
        config_path = scriptFolder + '/' + config_filename
        if not os.path.isfile(config_path):
            print("\nOops, looks like you've not setup a configuration.yaml file yet!")
            print("Tried to load: {}".format(config_path))
            print("   See the configuration.yaml.example to get you started\n")
            print("Check the wiki and/or website for help")
            print("   https://github.com/richibrics/PyMonitorMQTT/wiki - https://richibrics.github.io/PyMonitorMQTT/\n")
            print("Here's a list of options to get you started....")
            OutputAvailableEntities()
            exit(1)
        if len(sys.argv) == 1:
            # Run the main logic
            LoadYAML()
            SetupMonitors()
        else:
            # Additional command line logic
            x1 = sys.argv[1]
            # Very basic help command
            if (x1 == 'help') or (x1 == '-h') or (x1 == '--help') or (x1 == '--h'):
                OutputAvailableEntities()
                exit(1)

            print(
                "Run without arguments to start application or use --help to see available options")
    except Exception as exc:  # Main try except to give information about exception management
        logger = Logger(config)
        logger.Log(Logger.LOG_ERROR, 'Main',
                   ExceptionTracker.TrackString(exc))
        logger.Log(Logger.LOG_ERROR, 'Main',
                   'Try to check your configuration.yaml')
        logger.Log(Logger.LOG_ERROR, 'Main',
                   "If the problem persists, check issues (or open a new one) at 'https://github.com/richibrics/PyMonitorMQTT'")
        exit(1)
