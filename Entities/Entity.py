import datetime
from Logger import Logger, ExceptionTracker
import json
from Configurator import Configurator as cf
import sys
import yaml
import hashlib
from os import path
import consts


class Entity():
    import voluptuous 
    import consts
    import schemas
    from Settings import Settings
    from ValueFormatter import ValueFormatter
    from Logger import Logger, ExceptionTracker
    from Configurator import Configurator

    # To replace an original topic with a personalized one from configuration (may not be used).
    # When a sensor send the data with a topic, if the user choose a fixed topic in config,
    # then when I send the data I don't use the topic defined in the function but I replaced that
    # with the user's one that I store in this list of dict
    lastSendingTime = None
    lastDiscoveryTime = None


    def __init__(self, monitor_id, brokerConfigs, mqtt_client, send_interval, entityConfigs, logger, entityManager, entityType=None):  # Config is args
        self.initializeState=False
        self.postinitializeState=False

        self.name = self.GetEntityName(entityType)
        self.monitor_id = monitor_id

        self.replacedTopics = []
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

        # First thing: validate entity configuration and set the entity config to the validated config (with defaults)
        self.ValidateSchema()

        # Then load the options in the entity from the configuration file
        self.ParseOptions()

        self.Log(self.Logger.LOG_DEVELOPMENT,"Options founds:")
        self.Log(self.Logger.LOG_DEVELOPMENT,self.options)

        self.CallInitialize()

    def Initialize(self):  # Implemented in sub-classes
        pass

    def CallInitialize(self): 
        try:
            self.Initialize()
            self.initializeState=True
            self.Log(Logger.LOG_INFO,"Initialization successfully completed")
        except Exception as e:
            self.Log(Logger.LOG_ERROR,"Initialization interrupted due to an error")
            self.Log(Logger.LOG_ERROR,
                    ExceptionTracker.TrackString(e))
            del(self)
        

    # Implemented in sub-classes
    def Callback(self, message):  # Run by the OnMessageEvent
        pass


    def PostInitialize(self):  # Implemented in sub-classes
        pass

    def CallPostInitialize(self):  
        try:
            self.PostInitialize()
            self.postinitializeState=True
            self.Log(Logger.LOG_INFO,"Post-initialization successfully completed")
        except Exception as e:
            self.Log(Logger.LOG_ERROR,"Post-initialization interrupted due to an error")
            self.Log(Logger.LOG_ERROR,
                    ExceptionTracker.TrackString(e))
            del(self)


    
    # Function that returns the default schema if not implemented directly in each entity
    def EntitySchema(self): # Can be implemented in sub-entity
        return self.GetDefaultEntitySchema()


    def ValidateSchema(self):
        try:
            self.Log(Logger.LOG_INFO,"Validating configuration...")
            if self.entityConfigs is not None:
                self.entityConfigs = self.EntitySchema()(self.entityConfigs) # Validate with the entity config and set the entity config to the validated config (with defaults)
            self.Log(Logger.LOG_INFO,"Validation successfully completed")
        except Exception as e:
            self.Log(Logger.LOG_ERROR,"Error while validating entity configuration: " +str(e))
            raise Exception("Can't validate " + self.name + " configuration. Check your configuration.yaml file")

        
    # Can be edited from sub sensors to edit different options of the discovery data
    def ManageDiscoveryData(self, discovery_data):
        return discovery_data

    def ParseOptions(self):
        # I can have options both in broker configs and single sensor configs
        # At first I search in broker config. Then I check the per-sensor option and if I find
        # something there, I replace - if was set from first step -  broker configs (or simply add a new entry)

        for optionToSearch in self.consts.SCAN_OPTIONS: 
            # 1: Set from broker's configs
            if optionToSearch in self.brokerConfigs:
                if type(self.brokerConfigs[optionToSearch])==dict: # Id dict I have to copy to avoid errors
                    self.options[optionToSearch]=self.brokerConfigs[optionToSearch].copy()
                else:
                    self.options[optionToSearch]=self.brokerConfigs[optionToSearch]

            # 2: Set from entity's configs: join to previous value if was set
            if self.entityConfigs and optionToSearch in self.entityConfigs:
                if optionToSearch in self.options: # If I've just found this option in monitors config, then I have to add the entity config to the previous set options
                    self.options[optionToSearch]=self.JoinDictsOrLists(self.options[optionToSearch],self.entityConfigs[optionToSearch]) 
                else: # else I have only the entity config -> I set the option to that
                    self.options[optionToSearch]=self.entityConfigs[optionToSearch] 

    def GetOption(self, path, defaultReturnValue=None):
        return cf.GetOption(self.options, path, defaultReturnValue)

    def ListTopics(self):
        return self.outTopics

    def AddTopic(self, topic):
        self.outTopicsAddedNumber += 1
        # If user in options defined custom topics, store original and custom topic and replace it in the send function
        if self.GetOption(self.consts.CUSTOM_TOPICS_OPTION_KEY) is not None and len(self.GetOption(self.consts.CUSTOM_TOPICS_OPTION_KEY)) >= self.outTopicsAddedNumber:
            self.AddReplacedTopic(topic,self.GetOption(self.consts.CUSTOM_TOPICS_OPTION_KEY)[self.outTopicsAddedNumber-1])
            self.Log(Logger.LOG_INFO, 'Using custom topic defined in options')

        self.outTopics.append({'topic': topic, 'value': ""})

        self.Log(Logger.LOG_DEVELOPMENT, "Adding topic: " + topic)
        self.Log(Logger.LOG_DEVELOPMENT,
                 "Discovery topic normalizer: " + topic.replace("/", "_"))

    def SubscribeToTopic(self, topic):
        self.inTopics.append(topic)
        self.inTopicsAddedNumber += 1


        # If user in options defined custom topics, use them and not the one choosen in the command
        if self.GetOption(self.consts.CUSTOM_TOPICS_OPTION_KEY) and len(self.GetOption(self.consts.CUSTOM_TOPICS_OPTION_KEY)) >= self.inTopicsAddedNumber:
            original=topic
            topic = self.GetOption(self.consts.CUSTOM_TOPICS_OPTION_KEY)[
                self.inTopicsAddedNumber-1]
            self.AddReplacedTopic(original,topic) # Add to edited topics
            self.Log(Logger.LOG_INFO, 'Using custom topic defined in options')
        else: # If I don't have a custom topic for this, use the default topic format
            topic = self.FormatTopic(topic)

        self.mqtt_client.AddNewTopic(topic, self)

        # Log the topic as debug if user wants
        self.Log(Logger.LOG_DEBUG, 'Subscribed to topic: ' + topic)

        return topic  # Return the topic cause upper function should now that topic may have been edited


    def RemoveOutboundTopic(self,topic): # Should receive the element in the list outTopics: string with the original topic (like 'message_time')
        if type(topic) == str: # Not the topic,value combo -> get the combo
            for top in self.outTopics:
                if top['topic']==topic:
                    topic=top

        if topic in self.outTopics:
            self.outTopicsAddedNumber -= 1
            self.Log(Logger.LOG_DEBUG,"Removing topic: " + topic['topic'])
            self.outTopics.remove(topic)

    def RemoveInboundTopic(self,topic): # Should receive the element in the list inTopics: string with the original topic (like 'lock_command')
        if topic in self.inTopics:
            self.inTopicsAddedNumber-=1
            self.Log(Logger.LOG_DEBUG,"Unsubscribed to topic: " + topic)
            self.inTopics.remove(topic)
            self.mqtt_client.UnsubscribeToTopic(self.SelectTopic(topic)) # The client has to remove the full topic (customized)

    def AddReplacedTopic(self,original,custom):
        self.replacedTopics.append(
                {'original': original, 'custom': custom})

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


    # valueType, valueSize, forceValueFormatter are for the ValueFormatter and are not required
    def SetTopicValue(self, topic_name, value, valueType=None):
        # At first using topic string, I get his dict from topics list
        topic = self.GetTopicByName(topic_name)
        if topic:  # Found

            if valueType is not None:
                # If user defined in options he wants  size / unit of measurement (1200 [in Byte] -> 1,2KB)
                value = self.ValueFormatter.GetFormattedValue(value,valueType, self.GetValueFormatterOptionForTopic(topic_name))
                # I pass the options from format_value that I need 

            # Set the value
            topic['value'] = value
        else:  # Not found, log error
            self.Log(Logger.LOG_ERROR, 'Topic ' +
                     topic_name + ' does not exist !')

    def GetValueFormatterOptionForTopic(self,valueTopic): # Return the ValueFormat options for the passed topic
        VFoptions = self.GetOption(self.consts.VALUE_FORMAT_OPTION_KEY)
        # if the options are not in a list: specified options are for every topic
        if type(VFoptions) is not list:
            return VFoptions
        else: 
            # I have the same structure (topic with wildcard and configs) that I have for the topic settings in discovery
            for topicOptions in VFoptions:
                optionTopic = cf.GetOption(topicOptions,"topic")
                if optionTopic == "*" or optionTopic==valueTopic:
                    return topicOptions
            return None
        return None

    def CallUpdate(self):  # Call the Update method safely
        try:
            self.Update()
        except Exception as exc:
            self.Log(Logger.LOG_ERROR, 'Error occured during update')
            self.Log(Logger.LOG_ERROR, ExceptionTracker.TrackString(exc))
            self.entityManager.UnloadEntity(self)

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
            self.entityConfigs.UnloadEntity(self)

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
        model = self.consts.TOPIC_FORMAT
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
        return cf.GetOption(self.brokerConfigs, [self.consts.CONFIG_DISCOVERY_KEY, self.consts.DISCOVERY_ENABLE_KEY], False)

    # Calculate if a send_interval spent since the last sending time
    def ShouldSendDiscoveryConfig(self):
        # Check if Discovery is enabled
        if self.GetOption([self.consts.CONFIG_DISCOVERY_KEY, self.consts.DISCOVERY_ENABLE_KEY], False) is not False:
            # Not for don't send sensors
            if self.GetOption('dont_send') is True:
                return False # Don't send if disabled in config
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
        if suffix==None:
            suffix=self.consts.SENSOR_NAME_SUFFIX

        # Only SENSORCLASS (without Sensor suffix)
        if self.consts.SENSOR_NAME_SUFFIX in self.GetClassName():
            return self.GetClassName().split(self.consts.SENSOR_NAME_SUFFIX)[0]
        elif self.consts.COMMAND_NAME_SUFFIX in self.GetClassName():
            return self.GetClassName().split(self.consts.COMMAND_NAME_SUFFIX)[0]
        else:
            return self.GetClassName()

    def GetSendMessageInterval(self):
        return self.send_interval

    def GetSendDiscoveryConfigInterval(self):
        # Search in config or use default
        return self.GetOption([self.consts.CONFIG_DISCOVERY_KEY, self.consts.DISCOVERY_PUBLISH_INTERVAL_KEY], self.consts.DISCOVERY_PUBLISH_INTERVAL_DEFAULT)

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

    # Use this function to ask if a topic is in the replacedTopic list
    def TopicHadBeenReplaced(self,topic):
        for combo in self.replacedTopics:
            if combo['original']==topic:
                return True
        return False

    def LoadSettings(self):
        # 1: Get path of the single object
        # 2: If I dont find the yaml in that folder, I return None
        # 3: If I find it, I parse the yaml and I return the dict
        # Start:
        # 1
        settings_path = path.join(
            self.individualPath, self.consts.OBJECT_SETTINGS_FILENAME)
        # try 3 except 2
        try:
            with open(settings_path) as f:
                self.settings = yaml.load(f, Loader=yaml.FullLoader)
        except:
            self.settings = None

        return self.settings


    def PrepareDiscoveryPayloads(self):
        discovery_data = []

        # Check if Discovery is enabled
        if self.GetOption([self.consts.CONFIG_DISCOVERY_KEY, self.consts.DISCOVERY_ENABLE_KEY], False) is not False:
            # Okay need auto discovery

            # Not for don't send sensors
            if self.GetOption('dont_send') is True:
                return  # Don't send if disabled in config

            prefix = self.GetOption([
                                  self.consts.CONFIG_DISCOVERY_KEY, self.consts.DISCOVERY_DISCOVER_PREFIX_KEY], self.consts.DISCOVERY_DISCOVER_PREFIX_DEFAULT)
            preset = self.GetOption([
                                  self.consts.CONFIG_DISCOVERY_KEY, self.consts.DISCOVERY_PRESET_KEY])
            entity_preset_data = None

            if preset:
                # Check here if I have an entry in the discovery file for this topic and use that data (PLACE IN 'sensor_data')
                entity_preset_data = cf.GetOption(self.settings,[self.consts.SETTINGS_DISCOVERY_KEY, preset])  # THIS

            for topic in self.outTopics:
                # discoveryData: {name, config_topic, payload}
                # print(topic)
                data = self.PrepareTopicDiscoveryData(
                    topic['topic'], self.consts.TYPE_TOPIC_OUT, prefix, preset, entity_preset_data)
                if data:
                    discovery_data.append(data)

            for topic in self.inTopics:
                # discoveryData: {name, config_topic, payload}
                data = self.PrepareTopicDiscoveryData(
                    topic, self.consts.TYPE_TOPIC_IN, prefix, preset, entity_preset_data)
                if data:
                    discovery_data.append(data)

        return discovery_data


    def PrepareTopicDiscoveryData(self, topic, entity_model, prefix, preset, entity_preset_data):
        payload = {}
        topicSettings = None

        # Warning ! Discovery configuration for a single topic could be in: entity settings; user configuration

        # DISCOVERY DATA FROM ENTITY SETTINGS 
        # Look for custom discovery settings for this sensor, topic and preset:
        if entity_preset_data:
            for discoveryTopic in entity_preset_data:
                dtTopic = cf.GetOption(discoveryTopic, "topic")
                if (dtTopic == topic or dtTopic == "*") and cf.GetOption(discoveryTopic, self.consts.SETTINGS_DISCOVERY_PRESET_PAYLOAD_KEY):
                    # Found dict for this topic in this sensor for this preset: Place in the payload
                    topicSettings = discoveryTopic
                    payload = cf.GetOption(
                        discoveryTopic, self.consts.SETTINGS_DISCOVERY_PRESET_PAYLOAD_KEY).copy()

        # Check for Advanced information topic if I don't send advanced infomration: PS THIS IS USELESS CAUSE THIS TOPIC WON'T BE IN OUTTOPIC IN THAT CASE BUT IT'S BETTER TO CHECK
        # If I don't send advanced_information and the topic settings says the topic is advanced, I return None because this entity won't send any message on this topic
        if self.GetOption(self.consts.ADVANCED_INFO_OPTION_KEY,False)==False and cf.GetOption(topicSettings,[self.consts.SETTINGS_DISCOVERY_KEY,self.consts.SETTINGS_DISCOVERY_ADVANCED_TOPIC_KEY],False)==True:
            return None

        # DISCOVERY DATA FROM USER CONFIGURATION in entityConfig -> discovery -> settings

        # Take user_discovery_config not from options( thaht includes also monitors discovery config but oly from entity configs
        user_discovery_config=cf.ReturnAsList(cf.GetOption(self.entityConfigs,[self.consts.ENTITY_DISCOVERY_KEY,self.consts.ENTITY_DISCOVERY_PAYLOAD_KEY]),None) 
        if user_discovery_config:
            for user_topic_config in user_discovery_config:
                dtTopic=cf.GetOption(user_topic_config,"topic")
                if not dtTopic or dtTopic == topic or dtTopic == "*":     
                    # Copy all the configuration I have in the payload
                    for key, value in user_topic_config.items():
                        if key != "topic": # Avoid topic because is a non-payload information but only to recognise settings
                            payload[key]=value


        # If I have to disable, return None
        if cf.GetOption(topicSettings, self.consts.SETTINGS_DISCOVERY_PRESET_DISABLE_KEY, False):
            return None

        # Do I have the name in the  preset settings or do I set it using the default topic ?
        if not 'name' in payload:
            payload['name'] = topic.replace("/", "_")

        # Check and add this only if has option true
        if self.GetOption([self.consts.CONFIG_DISCOVERY_KEY, self.consts.DISCOVERY_NAME_PREFIX_KEY], self.consts.DISCOVERY_NAME_PREFIX_DEFAULT):
            payload['name'] = self.brokerConfigs['name'] + \
                " - " + payload['name']

        # Prepare the part of the config topic after the prefix and the sensortype 
        topic_component = self.TopicRemoveBadCharacters(self.SelectTopic(topic)) 

        payload['device'] = self.GetDiscoveryDeviceData()

        # Unique hashed
        payload['unique_id'] = hashlib.md5((self.SelectTopic(topic)).encode('utf-8')).hexdigest()

        if(entity_model == self.consts.TYPE_TOPIC_OUT):
            # Do I have the type in the sensor preset settings or do I set it to 'sensor' ?
            entity_type = cf.GetOption(
                topicSettings, self.consts.SETTINGS_DISCOVERY_PRESET_TYPE_KEY, "sensor")
            # Send the topic where the Sensor will send his state

            payload['expire_after']=self.GetOption([self.consts.CONFIG_DISCOVERY_KEY, self.consts.DISCOVERY_EXPIRE_AFTER_KEY], self.consts.DISCOVERY_EXPIRE_AFTER_DEFAULT)
            payload['state_topic'] = self.SelectTopic(topic)
        else:
            # Do I have the type in the sensor preset settings or do I set it to 'sensor' ?
            entity_type = cf.GetOption(
                topicSettings, self.consts.SETTINGS_DISCOVERY_PRESET_TYPE_KEY, "switch")
            # Send the topic where the Switch will receive the message
            payload['command_topic'] = self.SelectTopic(topic)


        # Compose the topic that will be used to send the disoovery configuration
        config_send_topic = self.consts.AUTODISCOVERY_TOPIC_CONFIG_FORMAT.format(
            prefix, entity_type, topic_component)

        return {"name": topic, "config_topic": config_send_topic, "payload": dict(payload)}

    def GetDiscoveryDeviceData(self):  # Add device information
        sw_info = self.Settings.GetInformation()
        device = {}
        device['name'] = "Monitor " + self.brokerConfigs['name']
        device['model'] = self.brokerConfigs['name']
        device['identifiers'] = self.brokerConfigs['name']
        try:
            device['manufacturer'] = sw_info['name']
            device['sw_version'] = sw_info['version']
        except:
            self.Log(Logger.LOG_WARNING,"No software information file found !")
        return device

    # discoveryData: {name, config_topic, payload}
    def PublishDiscoveryData(self, discovery_data):
        for discovery_entry in discovery_data:
            self.mqtt_client.SendTopicData(
                discovery_entry['config_topic'], json.dumps(discovery_entry['payload']))

    def TopicRemoveBadCharacters(self, string):
        return string.replace("/", "_").replace(" ", "_").replace("-", "_").lower()

    def Log(self, messageType, message):
        self.logger.Log(messageType, self.name + " Entity", message)

    def GetDefaultEntitySchema(self):
        return self.schemas.ENTITY_DEFAULT_SCHEMA

    # Used to scan the options and join the found options in the configuration.yaml to the default option value (which is the source)
    def JoinDictsOrLists(self,source,toJoin): # If source is a list, join toJoin to the list; if source is a dict, join toJoin keys and values to the source
        if type(source)==list:
            if type(toJoin)==list:
                return source+toJoin
            else:
                source.append(toJoin)
        elif type(source)==dict:
            if type(toJoin) ==dict:
                for key,value in toJoin.items():
                    source[key]=value
            else:
                source['no_key']=toJoin
            return source
        return toJoin # If no source recognized, return toJoin