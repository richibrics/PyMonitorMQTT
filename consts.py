SENSOR_NAME_SUFFIX = "Sensor"
COMMAND_NAME_SUFFIX = "Command"
SENSORS_MODULE_NAME = "Sensors"
COMMAND_MODULE_NAME = "Commands"

# Topic format
TOPIC_FORMAT = 'monitor/{}/{}'
AUTODISCOVERY_TOPIC_CONFIG_FORMAT="{}/{}/monitormqtt/{}/config"

CONFIG_COMMANDS_KEY = 'commands'
CONFIG_SENSORS_KEY = 'sensors'

INFORMATION_FILENAME = "information.json"

# To format value (1200000B -> 1,2GB)
FORMATTED_VALUE_DECIMALS = 2

# Lists of measure units
BYTE_SIZES = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

# Option parsers will look for these keys in config dicts
ADVANCED_INFO_OPTION_KEY = 'advanced_information'
FORMATTED_VALUES_OPTION_KEY = 'formatted_values'
CUSTOM_TOPICS_OPTION_KEY = 'custom_topics'
DONT_SEND_DATA_OPTION_KEY = 'dont_send'
DEBUG_OPTION_KEY = 'debug'
# For example notify takes title and message. Then here I will pass specifics dato for sensors/commands
CONTENTS_OPTION_KEY = 'contents'
POSSIBLE_OPTIONS = [DEBUG_OPTION_KEY, ADVANCED_INFO_OPTION_KEY,
                    FORMATTED_VALUES_OPTION_KEY, CUSTOM_TOPICS_OPTION_KEY, DONT_SEND_DATA_OPTION_KEY, CONTENTS_OPTION_KEY]

FIXED_VALUE_OS_MACOS = "macOS"
FIXED_VALUE_OS_WINDOWS = "Windows"
FIXED_VALUE_OS_LINUX = "Linux"

OBJECT_SETTINGS_FILENAME = "settings.yaml"

ONLINE_STATUS = "Online"
OFFLINE_STATUS = "Offline"

FILE_READ_SENSOR_FILENAME_CONTENTS_OPTION ="filename"

# LOGGER CONSTS
LOGGER_CONFIG_KEY = "logger"
# Split in more lines if message's too long
LOGGER_MESSAGE_WIDTH_KEY = "logger_message_width"
LOGGER_MESSAGE_WIDTH_DEFAULT = 40
LOGGER_FILE_LEVEL_KEY = "file_level"
LOGGER_CONSOLE_LEVEL_KEY = "console_level"
LOGGER_DEFAULT_LEVEL = 3

# DISCOVERY
DISCOVERY_KEY = "discovery"
DISCOVERY_ENABLE_KEY = "enable"
DISCOVERY_DISCOVER_PREFIX_KEY = "discover_prefix"
DISCOVERY_NAME_PREFIX_KEY = "name_prefix"
DISCOVERY_PUBLISH_INTERVAL_KEY = "publish_interval"
DISCOVERY_PRESET_KEY = "preset"
# Defaults
DISCOVERY_DISCOVER_PREFIX_DEFAULT = "monitor"
DISCOVERY_NAME_PREFIX_DEFAULT = False
DISCOVERY_PUBLISH_INTERVAL_DEFAULT = 30

# Sensor and command settings
SETTINGS_REQUIREMENTS_KEY = "requirements"
SETTINGS_REQUIREMENTS_SENSOR_KEY = "requirements"
SETTINGS_REQUIREMENTS_COMMAND_KEY = "requirements"

SETTINGS_DISCOVERY_KEY = "discovery"
SETTINGS_DISCOVERY_PRESET_PAYLOAD_KEY= "payload"
SETTINGS_DISCOVERY_PRESET_TYPE_KEY = "type"