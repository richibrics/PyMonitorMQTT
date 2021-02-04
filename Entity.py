import datetime
from Logger import Logger, ExceptionTracker
import json
from Configurator import Configurator as cf
import sys
import yaml
import hashlib
from os import path
from consts import *


class Entity():
    import consts
    from Settings import Settings
    from ValueFormatter import ValueFormatter
    from Logger import Logger, ExceptionTracker

    # To replace an original topic with a personalized one from configuration (may not be used).
    # When a sensor send the data with a topic, if the user choose a fixed topic in config,
    # then when I send the data I don't use the topic defined in the function but I replaced that
    # with the user's one that I store in this list of dict
    lastSendingTime = None
    lastDiscoveryTime = None
    replacedTopics = []

    def __init__(self, monitor_id, brokerConfigs, mqtt_client, send_interval, entityConfigs, logger, entityManager, entityType=SENSOR_NAME_SUFFIX):  # Config is args
        self.name = self.GetEntityName(entityType)
        self.monitor_id = monitor_id

        self.outTopics = []  # List of {topic, value}
        self.inTopics = []  # Only used for discovery, real used list is in the mqtt client where I have a list with topic-callback
        self.outTopicsAddedNumber = 0
        self.inTopicsAddedNumber = 0  # was subscribedTopics

        self.brokerConfigs = brokerConfigs
        self.entityConfigs = entityConfigs
        self.options = {}

        self.mqtt_client = mqtt_client
        self.send_interval = send_interval
        self.logger = logger
        self.entityManager = entityManager

        # Get for some features the pathof the folder cutting the py filename (abs path to avoid windows problems)
        self.individualPath = path.dirname(path.abspath(
            sys.modules[self.__class__.__module__].__file__))
        # Do per sensor operations
        self.ParseOptions()
        self.Initialize()

    def Initialize(self):  # Implemented in sub-classes
        pass

    # Implemented in sub-classes
    def Callback(self, message):  # Run by the OnMessageEvent
        pass

    def PostInitialize(self):  # Implemented in sub-classes
        pass

    # Can be edited from sub sensors to edit different options of the discovery data
    def ManageDiscoveryData(self, discovery_data):
        return discovery_data

    def ParseOptions(self):
        # I can have options both in broker configs and single sensor configs
        # At first I search in broker config. Then I check the per-sensor option and if I find
        # something there, I replace - if was set from first step -  broker configs (or simply add a new entry)

        for optionToSearch in POSSIBLE_OPTIONS:
            # 1: Set from broker's configs
            if optionToSearch in self.brokerConfigs:
                self.options[optionToSearch] = self.brokerConfigs[optionToSearch]

            # 2: Set from sensor's configs
            if self.entityConfigs and optionToSearch in self.entityConfigs:
                self.options[optionToSearch] = self.entityConfigs[optionToSearch]

    def GetOption(self, path, defaultReturnValue=None):
        return cf.GetOption(self.options, path, defaultReturnValue)

    def ListTopics(self):
        return self.outTopics

    def AddTopic(self, topic):
        self.outTopicsAddedNumber += 1
        # If user in options defined custom topics, store original and custom topic and replace it in the send function
        replaced = False
        if self.GetOption('custom_topics') is not None and len(self.GetOption('custom_topics')) >= self.outTopicsAddedNumber:
            self.replacedTopics.append(
                {'original': topic, 'custom': self.GetOption('custom_topics')[self.outTopicsAddedNumber-1]})
            self.Log(Logger.LOG_INFO, 'Using custom topic defined in options')
            replaced = True

        self.outTopics.append({'topic': topic, 'value': ""})

        self.Log(Logger.LOG_DEVELOPMENT, "Adding topic: " + topic)
        self.Log(Logger.LOG_DEVELOPMENT,
                 "Discovery topic normalizer: " + topic.replace("/", "_"))

    def GetFirstTopic(self):
        return self.outTopics[0]['topic'] if len(self.outTopics) else None

    def GetTopicByName(self, name):
        # Using topic string, I get his dict from topics list
        for topic in self.outTopics:
            if topic['topic'] == name:
                return topic
        return None

    def GetTopicValue(self, topic_name=None):
        if not topic_name:
            topic_name = self.GetFirstTopic()

        topic = self.GetTopicByName(topic_name)
        if topic:
            return topic['value']
        else:
            return None

    def SetTopicValue(self, topic_name, value, valueType=ValueFormatter.TYPE_NONE):
        # At first using topic string, I get his dict from topics list
        topic = self.GetTopicByName(topic_name)
        if topic:  # Found

            # If user defined in options he wants formatted values (1200,byte -> 1,2KB)
            if self.GetOption('formatted_values'):
                value = ValueFormatter.GetFormattedValue(value, valueType)

            # Set the value
            topic['value'] = value
        else:  # Not found, log error
            self.Log(Logger.LOG_ERROR, 'Topic ' +
                     topic_name + ' does not exist !')

    def CallUpdate(self):  # Call the Update method safely
        try:
            self.Update()
        except Exception as exc:
            self.Log(Logger.LOG_ERROR, 'Error occured during update')
            self.Log(Logger.LOG_ERROR, ExceptionTracker.TrackString(exc))
            self.entityManager.UnloadEntity(self.name, self.monitor_id)

    def Update(self):  # Implemented in sub-classes - Here values are taken
        self.Log(Logger.LOG_WARNING, 'Update method not implemented')
        pass  # Must not be called directly, cause stops everything in exception, call only using CallUpdate

    def CallCallback(self, message):  # Safe method to run the Callback
        try:
            self.Log(Logger.LOG_INFO, 'Command actioned')
            self.Callback(message)
        except Exception as exc:
            self.Log(Logger.LOG_ERROR, 'Error occured in callback: '+str(exc))
            self.Log(Logger.LOG_ERROR, ExceptionTracker.TrackString(exc))
            self.commandManager.UnloadCommand(self.name, self.monitor_id)

    def SelectTopic(self, topic):
        # for a topic look for its customized topic and return it if there's. Else return the default one but completed with FormatTopic

        if(type(topic) == dict):
            checkTopic = topic['topic']
        else:
            checkTopic = topic

        for customs in self.replacedTopics:
            # If it's in the list of topics to replace
            if checkTopic == customs['original']:
                return customs['custom']

        return self.FormatTopic(checkTopic)

    def SendData(self):
        if self.GetOption('dont_send') is True:
            return  # Don't send if disabled in config

        if self.mqtt_client is not None:
            for topic in self.outTopics:  # Send data for all topic

                # For each topic I check if I send to that or if it has to be replaced with a custom topic defined in options
                topicToUse = self.SelectTopic(topic)

                # Log the topic as debug if it's on
                if 'debug' in self.brokerConfigs and self.brokerConfigs['debug'] is True:
                    self.Log(Logger.LOG_DEBUG, "Sending data to " + topicToUse)

                self.mqtt_client.SendTopicData(
                    topicToUse, topic['value'])

    def SubscribeToTopic(self, topic):
        self.inTopics.append(topic)
        self.inTopicsAddedNumber += 1

        topic = self.FormatTopic(topic)

        # If user in options defined custom topics, use them and not the one choosen in the command
        if self.GetOption(CUSTOM_TOPICS_OPTION_KEY) and len(self.GetOption(CUSTOM_TOPICS_OPTION_KEY)) >= self.inTopicsAddedNumber:
            topic = self.GetOption(CUSTOM_TOPICS_OPTION_KEY)[
                self.inTopicsAddedNumber-1]
            self.Log(Logger.LOG_INFO, 'Using custom topic defined in options')

        self.mqtt_client.AddNewTopic(topic, self)

        # Log the topic as debug if user wants
        if self.GetOption(DEBUG_OPTION_KEY):
            self.Log(Logger.LOG_DEBUG, 'Subscribed to topic: ' + topic)

        return topic  # Return the topic cause upper function should now that topic may have been edited

    def FindEntities(self, name):  # Find active entities for some specific action
        if(self.entityManager):
            return self.entityManager.FindEntities(name, self.monitor_id)
        else:
            self.Log(Logger.LOG_ERROR,
                     'EntityManager not set!')
        return None

    def FindEntity(self, name):  # Return first found entity from FindEntities
        if(self.entityManager):
            entities = self.FindEntities(name)
            if(len(entities)):
                return entities[0]
            else:
                return None
        else:
            self.Log(Logger.LOG_ERROR,
                     'EntityManager not set!')
        return None

    def FormatTopic(self, last_part_of_topic):
        model = TOPIC_FORMAT
        if 'topic_prefix' in self.brokerConfigs:
            model = self.brokerConfigs['topic_prefix'] + '/'+model
        return model.format(self.brokerConfigs['name'], last_part_of_topic)

    # Calculate if a send_interval spent since the last sending time
    def ShouldSendMessage(self):
        if self.outTopicsAddedNumber == 0:
            return False

        if self.GetLastSendingTime() is None:  # Never sent anything
            return True  # Definitely yes, you should send
        else:
            # Calculate time elapsed
            # Get current time
            now = datetime.datetime.now()
            # Calculate
            seconds_elapsed = (now-self.GetLastSendingTime()).total_seconds()
            # Check if now I have to send
            if seconds_elapsed >= self.GetSendMessageInterval():
                return True
            else:
                return False

    def IsDiscoveryEnabled(self):
        return cf.GetOption(self.brokerConfigs, [DISCOVERY_KEY, DISCOVERY_ENABLE_KEY], False)

    # Calculate if a send_interval spent since the last sending time
    def ShouldSendDiscoveryConfig(self):
        # Check if Discovery is enabled
        if cf.GetOption(self.brokerConfigs, [DISCOVERY_KEY, DISCOVERY_ENABLE_KEY], False) is not False:
            if self.GetLastDiscoveryTime() is None:  # Never sent anything
                return True  # Definitely yes, you should send
            else:
                # Calculate time elapsed
                # Get current time
                now = datetime.datetime.now()
                # Calculate
                seconds_elapsed = (
                    now-self.GetLastDiscoveryTime()).total_seconds()
                # Check if now I have to send
                if seconds_elapsed >= self.GetSendDiscoveryConfigInterval():
                    return True
                else:
                    return False
        else:
            return False

    # Save the time when last message is sent. If no time passed, will be used current time
    def SaveTimeMessageSent(self, time=None):
        if time is not None:
            self.lastSendingTime = time
        else:
            self.lastSendingTime = datetime.datetime.now()

    def SaveTimeDiscoverySent(self, time=None):
        if time is not None:
            self.lastDiscoveryTime = time
        else:
            self.lastDiscoveryTime = datetime.datetime.now()

    def GetClassName(self):
        # Sensor.SENSORFOLDER.SENSORCLASS
        return self.__class__.__name__

    def GetEntityName(self, suffix):
        # Only SENSORCLASS (without Sensor suffix)
        return self.GetClassName().split('.')[-1].split(suffix)[0]

    def GetSendMessageInterval(self):
        return self.send_interval

    def GetSendDiscoveryConfigInterval(self):
        # Search in config or use default
        return cf.GetOption(self.brokerConfigs, [DISCOVERY_KEY, DISCOVERY_PUBLISH_INTERVAL_KEY], DISCOVERY_PUBLISH_INTERVAL_DEFAULT)

    def GetMqttClient(self):
        return self.mqtt_client

    def GetLogger(self):
        return self.logger

    def GetMonitorID(self):
        return self.monitor_id

    def GetLastSendingTime(self):
        return self.lastSendingTime

    def GetLastDiscoveryTime(self):
        return self.lastDiscoveryTime

    def LoadSettings(self):
        # 1: Get path of the single object
        # 2: If I dont find the yaml in that folder, I return None
        # 3: If I find it, I parse the yaml and I return the dict
        # Start:
        # 1
        settings_path = path.join(
            self.individualPath, OBJECT_SETTINGS_FILENAME)
        # try 3 except 2
        try:
            with open(settings_path) as f:
                self.settings = yaml.load(f, Loader=yaml.FullLoader)
        except:
            self.settings = None

        return self.settings

    def PrepareDiscoveryPayloads(self):
        payload = None
        discovery_data = []

        # Check if Discovery is enabled
        if cf.GetOption(self.brokerConfigs, [DISCOVERY_KEY, DISCOVERY_ENABLE_KEY], False) is not False:
            # Okay need auto discovery

            # Not for don't send sensors
            if self.GetOption('dont_send') is True:
                return  # Don't send if disabled in config

            prefix = cf.GetOption(self.brokerConfigs, [
                                  DISCOVERY_KEY, DISCOVERY_DISCOVER_PREFIX_KEY], DISCOVERY_DISCOVER_PREFIX_DEFAULT)
            preset = cf.GetOption(self.brokerConfigs, [
                                  DISCOVERY_KEY, DISCOVERY_PRESET_KEY])
            entity_preset_data = None
            topic_data = None

            if preset:
                # Check here if I have an entry in the discovery file for this topic and use that data (PLACE IN 'sensor_data')
                entity_preset_data = cf.GetOption(
                    self.settings, [SETTINGS_DISCOVERY_KEY, preset])  # THIS

            for topic in self.outTopics:
                # discoveryData: {name, config_topic, payload}
                # print(topic)
                data = self.PrepareTopicDiscoveryData(
                    topic['topic'], TYPE_TOPIC_OUT, prefix, preset, entity_preset_data)
                if data:
                    discovery_data.append(data)

            for topic in self.inTopics:
                # discoveryData: {name, config_topic, payload}
                data = self.PrepareTopicDiscoveryData(
                    topic, TYPE_TOPIC_IN, prefix, preset, entity_preset_data)
                if data:
                    discovery_data.append(data)

        return discovery_data

    def PrepareTopicDiscoveryData(self, topic, entity_model, prefix, preset, entity_preset_data):
        payload = {}
        topicSettings = None

        # Look for custom discovery settings for this sensor, topic and preset:
        if entity_preset_data:
            for discoveryTopic in entity_preset_data:
                dtTopic = cf.GetOption(discoveryTopic, "topic")
                if (dtTopic == topic or dtTopic == "*") and cf.GetOption(discoveryTopic, SETTINGS_DISCOVERY_PRESET_PAYLOAD_KEY):
                    # Found dict for this topic in this sensor for this preset: Place in the payload
                    topicSettings = discoveryTopic
                    payload = cf.GetOption(
                        discoveryTopic, SETTINGS_DISCOVERY_PRESET_PAYLOAD_KEY).copy()

        # If I have to disable, return None
        if cf.GetOption(topicSettings, self.consts.SETTINGS_DISCOVERY_PRESET_DISABLE_KEY, False):
            return None

        # Do I have the name in the  preset settings or do I set it using the default topic ?
        if not 'name' in payload:
            payload['name'] = topic.replace("/", "_")

        # Check and add this only if has option true
        if cf.GetOption(self.brokerConfigs, [DISCOVERY_KEY, DISCOVERY_NAME_PREFIX_KEY], DISCOVERY_NAME_PREFIX_DEFAULT):
            payload['name'] = self.brokerConfigs['name'] + \
                " - " + payload['name']

        # Prepare the part of the config topic where you place the component id
        topic_component = self.TopicRemoveBadCharacters(
            self.brokerConfigs['name']+"_"+topic)

        payload['device'] = self.GetDiscoveryDeviceData()
        payload['unique_id'] = hashlib.md5(topic.encode('utf-8')).hexdigest()

        if(entity_model == TYPE_TOPIC_OUT):
            # Do I have the type in the sensor preset settings or do I set it to 'sensor' ?
            entity_type = cf.GetOption(
                topicSettings, SETTINGS_DISCOVERY_PRESET_TYPE_KEY, "sensor")
            # Send the topic where the Sensor will send his state
            payload['state_topic'] = self.SelectTopic(topic)
        else:
            # Do I have the type in the sensor preset settings or do I set it to 'sensor' ?
            entity_type = cf.GetOption(
                topicSettings, SETTINGS_DISCOVERY_PRESET_TYPE_KEY, "switch")
            # Send the topic where the Switch will receive the message
            payload['command_topic'] = self.SelectTopic(topic)


        # Last thing: if StateSensor is loaded, use that to publish availability
        stateSensor=self.FindEntity("State")
        if(stateSensor):
            payload['availability_topic']=stateSensor.SelectTopic(stateSensor.GetFirstTopic())
            payload['payload_available']=self.consts.ONLINE_STATE
            payload['payload_not_available']=self.consts.OFFLINE_STATE



        # Compose the topic that will be used to send the disoovery configuration
        config_send_topic = AUTODISCOVERY_TOPIC_CONFIG_FORMAT.format(
            prefix, entity_type, topic_component)

        return {"name": topic, "config_topic": config_send_topic, "payload": dict(payload)}

    def GetDiscoveryDeviceData(self):  # Add device information
        sw_info = self.Settings.GetInformation()
        device = {}
        device['name'] = "Monitor " + self.brokerConfigs['name']
        try:
            device['manufacturer'] = sw_info['name']
            device['model'] = sw_info['name']
            device['identifiers'] = sw_info['name']
            device['sw_version'] = sw_info['version']
        except:
            self.Log(Logger.LOG_WARNING,"No software information file found ")
        return device

    # discoveryData: {name, config_topic, payload}
    def PublishDiscoveryData(self, discovery_data):
        for discovery_entry in discovery_data:
            self.mqtt_client.SendTopicData(
                discovery_entry['config_topic'], json.dumps(discovery_entry['payload']))

    def TopicRemoveBadCharacters(self, string):
        return string.replace("/", "_").replace(" ", "_").replace("-", "_").lower()

    def Log(self, messageType, message):
        self.logger.Log(messageType, self.name+' Sensor', message)
