from consts import *
from voluptuous import *
import voluptuous

ROOT_SCHEMA = Schema({})

VALUE_FORMAT_SCHEMA = Schema({
    
})

ENTITY_DEFAULT_SCHEMA = Schema({
    Optional(ADVANCED_INFO_OPTION_KEY, default=ADVANCED_INFO_OPTION_DEFAULT): bool,
    Optional(CUSTOM_TOPICS_OPTION_KEY, default=CUSTOM_TOPICS_OPTION_DEFAULT): [str]
})
