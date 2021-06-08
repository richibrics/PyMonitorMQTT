from consts import *
from voluptuous import *
import voluptuous

# where in defaults I put (for example) MONITOR_VALUE_FORMAT_SCHEMA({}), in MONITOR_VALUE_FORMAT_SCHEMA I must not have required 
# fields because then I can't use the ({}) system for default in the parent schema

# ROOT

# Root schema will be validated at start, each entity schema will be validated at entity init

MONITOR_VALUE_FORMAT_SCHEMA = Schema({
    Optional(VALUEFORMATTER_OPTIONS_UNIT_OF_MEASUREMENT_KEY, default=VALUEFORMATTER_OPTIONS_UNIT_OF_MEASUREMENT_DEFAULT): bool,
    Optional(VALUEFORMATTER_OPTIONS_DECIMALS_KEY, default=VALUEFORMATTER_OPTIONS_DECIMALS_DEFAULT): int,
    Optional(VALUEFORMATTER_OPTIONS_SIZE_KEY, default=VALUEFORMATTER_OPTIONS_SIZE_DEFAULT): Or(str,False)
})

MONITOR_LOGGER_SCHEMA = Schema({
    Optional(LOGGER_MESSAGE_WIDTH_KEY,default=LOGGER_MESSAGE_WIDTH_DEFAULT): int,
    Optional(LOGGER_FILE_LEVEL_KEY,default=LOGGER_DEFAULT_LEVEL): int,
    Optional(LOGGER_CONSOLE_LEVEL_KEY,default=LOGGER_DEFAULT_LEVEL): int
})

MONITOR_DISCOVERY_SCHEMA = Schema({
    Required(DISCOVERY_ENABLE_KEY): bool,
    Required(DISCOVERY_PRESET_KEY): str,
    Optional(DISCOVERY_DISCOVER_PREFIX_KEY, default=DISCOVERY_DISCOVER_PREFIX_DEFAULT): str, 
    Optional(DISCOVERY_NAME_PREFIX_KEY, default=False): bool,
    Optional(DISCOVERY_PUBLISH_INTERVAL_KEY, default=DISCOVERY_NAME_PREFIX_DEFAULT): int,
    Optional(DISCOVERY_EXPIRE_AFTER_KEY): int
})


MONITOR_SCHEMA = Schema({
    Required(CONFIG_BROKER_KEY): str,

    Optional(CONFIG_PORT_KEY,default=CONFIG_PORT_DEFAULT): int,
    
    Required(CONFIG_NAME_KEY): str,
    Optional(CONFIG_MQTT_ID_KEY): str, 
    Optional(CONFIG_SEND_INTERVAL_KEY, default=SEND_INTERVAL_DEFAULT): int, 

    Optional(CONFIG_USERNAME_KEY): str,
    Optional(CONFIG_PASSWORD_KEY): str, 

    Optional(CONFIG_DISCOVERY_KEY): MONITOR_DISCOVERY_SCHEMA,

    Optional(ADVANCED_INFO_OPTION_KEY, default=ADVANCED_INFO_OPTION_DEFAULT): bool,
    Optional(CUSTOM_TOPICS_OPTION_KEY, default=CUSTOM_TOPICS_OPTION_DEFAULT):  Or(str,[str]),
    Optional(DONT_SEND_DATA_OPTION_KEY, default=DONT_SEND_DATA_OPTION_DEFAULT): bool,
    Optional(VALUE_FORMAT_OPTION_KEY, default=MONITOR_VALUE_FORMAT_SCHEMA({})): MONITOR_VALUE_FORMAT_SCHEMA,

    Optional(CONFIG_SENSORS_KEY,default=[]): [Or(str,dict)],
    Optional(CONFIG_COMMANDS_KEY,default=[]): [Or(str,dict)]
})


ROOT_SCHEMA = Schema({
    Required(CONFIG_MONITORS_KEY): [MONITOR_SCHEMA],
    Optional(LOGGER_CONFIG_KEY,default=MONITOR_LOGGER_SCHEMA({})): MONITOR_LOGGER_SCHEMA
})


# ENTITY SCHEMAS 

# Part of the entity schemas where I have schemas with same values as before but without defaults: defaults are the configuration from the monitor schemas upper

ENTITY_VALUE_FORMAT_SCHEMA = Schema({
    Optional(VALUEFORMATTER_OPTIONS_UNIT_OF_MEASUREMENT_KEY): bool,
    Optional(VALUEFORMATTER_OPTIONS_DECIMALS_KEY): int,
    Optional(VALUEFORMATTER_OPTIONS_SIZE_KEY): Or(str,False)
})


ENTITY_DISCOVERY_SCHEMA = Schema({
    Optional(DISCOVERY_ENABLE_KEY): bool,
    Optional(DISCOVERY_PRESET_KEY): str,
    Optional(DISCOVERY_DISCOVER_PREFIX_KEY): str, 
    Optional(DISCOVERY_NAME_PREFIX_KEY): bool,
    Optional(DISCOVERY_PUBLISH_INTERVAL_KEY): int,
    Optional(SETTINGS_DISCOVERY_EXPIRE_AFTER_KEY): int,
    Optional(ENTITY_DISCOVERY_PAYLOAD_KEY): Or(dict,list)  # Where I can put the name for the entity in the hub and the custom icon without editing the entity code
})



ENTITY_DEFAULT_SCHEMA = Schema({ # No default here (only custom topics), will be used monitor config if not set here
    Optional(ADVANCED_INFO_OPTION_KEY): bool,
    Optional(CUSTOM_TOPICS_OPTION_KEY, default=CUSTOM_TOPICS_OPTION_DEFAULT):  Or(str,[str]),
    Optional(DONT_SEND_DATA_OPTION_KEY): bool,
    Optional(VALUE_FORMAT_OPTION_KEY): ENTITY_VALUE_FORMAT_SCHEMA,
    Optional(ENTITY_DISCOVERY_KEY): ENTITY_DISCOVERY_SCHEMA
})