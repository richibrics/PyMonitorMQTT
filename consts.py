# Topic format
TOPIC_FORMAT = 'monitor/{}/{}'
CONFIG_COMMANDS_KEY = 'commands'
CONFIG_SENSORS_KEY = 'sensors'

# Split in more lines if message's too long
DEFAULT_LOGGER_MESSAGE_WIDTH = 40

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
# For excample notify takes title and message. Then here I will pass specifics dato for sensors/commands
CONTENTS_OPTION_KEY = 'contents'
POSSIBLE_OPTIONS = [DEBUG_OPTION_KEY, ADVANCED_INFO_OPTION_KEY,
                    FORMATTED_VALUES_OPTION_KEY, CUSTOM_TOPICS_OPTION_KEY, DONT_SEND_DATA_OPTION_KEY, CONTENTS_OPTION_KEY]

FIXED_VALUE_OS_MACOS = "macOS"
FIXED_VALUE_OS_WINDOWS = "Windows"
FIXED_VALUE_OS_LINUX = "Linux"

OBJECT_REQUIREMENTS_FILENAME = "requirements.yaml"