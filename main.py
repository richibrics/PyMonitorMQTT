import os
import yaml
import time
from Logger import Logger, ExceptionTracker
from EntityManager import EntityManager
import sys
from Monitor import Monitor
from Entities.ClassManager import ClassManager

config = None
config_filename = 'configuration.yaml'

scriptFolder = str(os.path.dirname(os.path.realpath(__file__)))


def LoadYAML():
    global config
    with open(os.path.join(scriptFolder, config_filename)) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)


def SetupMonitors():
    # Setup manager
    entityManager = EntityManager(
        config)

    # If I have not a list of monitors, I setup only a monitor
    if ('monitors' not in config):
        monitor = Monitor(config, config, entityManager)
    else:  # More Monitors
        # Now setup monitors
        monitor_id = 0
        for monitor_config in config['monitors']:
            monitor_id += 1
            monitor = Monitor(monitor_config, config,
                              entityManager, monitor_id)

    # Start sensors loop
    entityManager.Start()


def output_available_modules():
    parse_module_prefixes = [
        'Sensors',
        'Commands',
    ]
    build_output = {}
    # Loop through the loaded Python modules in memory
    for look_up in sys.modules.keys():
        # Split the module name into pieces
        # Commands.TurnOffMonitorsCommand.TurnOffMonitorsCommand
        split_module_name = look_up.split(
            '.')  # 0 = Commands, 1 = TurnOffMonitorsCommand, 2 = TurnOffMonitorsCommand
        if len(split_module_name) < 3:
            continue

        # Is Commands not in the our lookup prefix (false)
        if split_module_name[0] not in parse_module_prefixes:
            continue

        root_topic = split_module_name[0]  # Root level (Commands)

        # Have we seen this root level before?
        if root_topic not in build_output:
            # Create empty placeholder for output
            build_output[root_topic] = []

        available_command = split_module_name[2]  # TurnOffMonitorsCommand

        # Is the root topic plural (Commands) , if so remove it.. we need this to trim the end command
        trim_prefix = split_module_name[0]
        if trim_prefix.endswith('s'):
            trim_prefix = trim_prefix[0:-1]  # (Command)

        available_command = available_command.replace(
            trim_prefix, '')  # (TurnOffMonitors)

        build_output[root_topic].append(available_command)

    if len(build_output) == 0:
        raise Exception('No modules loaded')

    for root_type in build_output.keys():
        print("{} options:".format(root_type))
        for option in build_output[root_type]:
            print("   - {}".format(option))


if __name__ == "__main__":
    #try:
    # Do we have a config file?
    config_path = scriptFolder + '/' + config_filename
    cm = ClassManager()
    cm.LoadAllEntities()
    if not os.path.isfile(config_path):
        print("\nOops, looks like you've not setup a configuration.yaml file yet!")
        print("Tried to load: {}".format(config_path))
        print("   See the configuration.yaml.example to get you started\n")
        print("Check the wiki and/or website for help")
        print("   https://github.com/richibrics/PyMonitorMQTT/wiki - https://richibrics.github.io/PyMonitorMQTT/\n")
        print("Here's a list of options to get you started....")
        output_available_modules()
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
            output_available_modules()
            exit(1)

        print(
            "Run without arguments to start application or use --help to see available options")
    '''
    except Exception as exc:  # Main try except to give information about exception management
        logger = Logger(config)
        logger.Log(Logger.LOG_ERROR, 'Main',
                   ExceptionTracker.TrackString(exc))
        logger.Log(Logger.LOG_ERROR, 'Main',
                   'Try to check your configuration.yaml')
        logger.Log(Logger.LOG_ERROR, 'Main',
                   "If the problem persists, check issues (or open a new one) at 'https://github.com/richibrics/PyMonitorMQTT'")
        exit(1)
    '''        
