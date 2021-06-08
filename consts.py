SENSOR_NAME_SUFFIX = "Sensor"
COMMAND_NAME_SUFFIX = "Command"

SEND_INTERVAL_DEFAULT = 20

TYPE_TOPIC_IN = 0
TYPE_TOPIC_OUT = 1

# Topic format
TOPIC_FORMAT = 'monitor/{}/{}'
AUTODISCOVERY_TOPIC_CONFIG_FORMAT = "{}/{}/monitormqtt/{}/config"

CONFIG_MONITORS_KEY = "monitors"

# Inside monitor keys
CONFIG_COMMANDS_KEY = 'commands'
CONFIG_SENSORS_KEY = 'sensors'
CONFIG_BROKER_KEY = 'broker'
CONFIG_PORT_KEY = 'port'
CONFIG_NAME_KEY = 'name'
CONFIG_SEND_INTERVAL_KEY = 'send_interval'
CONFIG_USERNAME_KEY = 'username'
CONFIG_PASSWORD_KEY = 'password'
CONFIG_MQTT_ID_KEY = 'mqtt_id'
CONFIG_DISCOVERY_KEY = "discovery"

CONFIG_PORT_DEFAULT = 1883


INFORMATION_FILENAME = "information.json"


# Option parsers will look for these keys in config dicts
ADVANCED_INFO_OPTION_KEY = 'advanced_information' # Extra info from sensors
ADVANCED_INFO_OPTION_DEFAULT = False

CUSTOM_TOPICS_OPTION_KEY = 'custom_topics' # To set custom topics to sensors/commands
CUSTOM_TOPICS_OPTION_DEFAULT = []

DONT_SEND_DATA_OPTION_KEY = 'dont_send' # Don't send sensors values and autodiscovery config
DONT_SEND_DATA_OPTION_DEFAULT = False

VALUE_FORMAT_OPTION_KEY = 'value_format' # Dict where user can place the VALUEFORMATTER_OPTIONS_x
VALUE_FORMAT_OPTION_DEFAULT = {}

CONTENTS_OPTION_KEY = 'contents' # To pass extra options to sensors (example: notify receives message and title with this)
CONTENTS_OPTION_DEFAULT = {}

# list of tuples key,default
SCAN_OPTIONS = [
    ADVANCED_INFO_OPTION_KEY,
    CUSTOM_TOPICS_OPTION_KEY,
    DONT_SEND_DATA_OPTION_KEY,
    VALUE_FORMAT_OPTION_KEY,
    CONTENTS_OPTION_KEY,
    CONFIG_DISCOVERY_KEY
]

# Removed DEBUG mode because you only need to set the console/file level to debug or upper

FIXED_VALUE_OS_MACOS = "macOS"
FIXED_VALUE_OS_WINDOWS = "Windows"
FIXED_VALUE_OS_LINUX = "Linux"

OBJECT_SETTINGS_FILENAME = "settings.yaml"

ONLINE_STATE = "Online"
OFFLINE_STATE = "Offline"


# LOGGER CONSTS
LOGGER_CONFIG_KEY = "logger"
# Split in more lines if message's too long
LOGGER_MESSAGE_WIDTH_KEY = "logger_message_width"
LOGGER_MESSAGE_WIDTH_DEFAULT = 40
LOGGER_FILE_LEVEL_KEY = "file_level"
LOGGER_CONSOLE_LEVEL_KEY = "console_level"
LOGGER_DEFAULT_LEVEL = 3

# DISCOVERY
DISCOVERY_ENABLE_KEY = "enable"
DISCOVERY_DISCOVER_PREFIX_KEY = "discover_prefix"
DISCOVERY_NAME_PREFIX_KEY = "name_prefix"
DISCOVERY_PUBLISH_INTERVAL_KEY = "publish_interval"
DISCOVERY_PRESET_KEY = "preset"
DISCOVERY_EXPIRE_AFTER_KEY = "expire_after" 

# Defaults
DISCOVERY_DISCOVER_PREFIX_DEFAULT = "monitor"
DISCOVERY_NAME_PREFIX_DEFAULT = False
DISCOVERY_PUBLISH_INTERVAL_DEFAULT = 30

# Should be greater than twice the publish interval
# It's the time after sensors are unavailable if not messages are received in these seconds
DISCOVERY_EXPIRE_AFTER_DEFAULT = 60 

# Sensor and command settings
SETTINGS_REQUIREMENTS_KEY = "requirements"
SETTINGS_REQUIREMENTS_SENSOR_KEY = "sensors"
SETTINGS_REQUIREMENTS_COMMAND_KEY = "commands"

# where in the entity settings, options like payload, sensor type and topic will be placed
SETTINGS_DISCOVERY_KEY = "discovery"
SETTINGS_DISCOVERY_PRESET_PAYLOAD_KEY = "payload"
SETTINGS_DISCOVERY_PRESET_TYPE_KEY = "type"
SETTINGS_DISCOVERY_PRESET_DISABLE_KEY = "disable"
SETTINGS_DISCOVERY_EXPIRE_AFTER_KEY = DISCOVERY_EXPIRE_AFTER_KEY # must be the same of the monitor one (so Entity.GetOption will use it's priority) 

SETTINGS_DISCOVERY_ADVANCED_TOPIC_KEY = "advanced_topic"

# Where in the user configuration the custom PAYLOAD will be placed
ENTITY_DISCOVERY_KEY = "discovery"
ENTITY_DISCOVERY_PAYLOAD_KEY = "settings"

ENTITIES_PATH = "Entities"
CUSTOM_ENTITIES_PATH = "Custom"

ON_STATE = "On"
OFF_STATE = "Off"



# Lists of measure units
BYTE_SIZES = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

# In the user config for sensor:
FORMATTED_VALUE_SIZE_OPTION_KEY = "size"
# "size" can be set to these:
SIZE_BYTE = "B"
SIZE_KILOBYTE = "KB"
SIZE_MEGABYTE = "MB"
SIZE_GIGABYTE = "GB"
SIZE_TERABYTE = "TB"


# Boolean value to add or not the unit to the end of the value
VALUEFORMATTER_OPTIONS_UNIT_OF_MEASUREMENT_KEY = "unit_of_measurement"
# only for Xbytes: If I have 1GB but I want the values as MB, setting size to SIZE_MEGABYTE, will send 1000MB
VALUEFORMATTER_OPTIONS_SIZE_KEY = "size"
# Number of decimals for the numeric value
VALUEFORMATTER_OPTIONS_DECIMALS_KEY = "decimals"

# Default values
VALUEFORMATTER_OPTIONS_DECIMALS_DEFAULT = 2
VALUEFORMATTER_OPTIONS_SIZE_DEFAULT = False # None is Disabled
VALUEFORMATTER_OPTIONS_UNIT_OF_MEASUREMENT_DEFAULT = False
