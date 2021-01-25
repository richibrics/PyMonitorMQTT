import datetime
from consts import *
import Logger
import json
from Configurator import Configurator as cf
import sys
import yaml
from ValueFormatter import ValueFormatter
from os import path


class Sensor():
    # To replace an original topic with a personalized one from configuration (may not be used).
    # When a sensor send the data with a topic, if the user choose a fixed topic in config,
    # then when I send the data I don't use the topic defined in the function but I replaced that
    # with the user's one that I store in this list of dict
    lastSendingTime = None
    lastDiscoveryTime = None
    replacedTopics = []

    def __init__(self, monitor_id, brokerConfigs, mqtt_client, send_interval, sensorConfigs, logger, sensorManager):  # Config is args
        self.topics = []  # List of {topic, value}
        self.options = {}
        self.monitor_id = monitor_id
        self.brokerConfigs = brokerConfigs
        self.mqtt_client = mqtt_client
        self.send_interval = send_interval
        self.sensorConfigs = sensorConfigs
        self.logger = logger
        self.sensorManager = sensorManager
        self.name = self.GetSensorName()
        self.addedTopics = 0
        # Get for some features the pathof the folder cutting the py filename (abs path to avoid windows problems)
        self.sensorPath = path.dirname(path.abspath(
            sys.modules[self.__class__.__module__].__file__))
        # Do per sensor operations
        self.ParseOptions()
        self.Initialize()

    def Initialize(self):  # Implemented in sub-classes
        pass

    def PostInitialize(self):  # Implemented in sub-classes
        pass

    def ParseOptions(self):
        # I can have options both in broker configs and single sensor configs
        # At first I search in broker config. Then I check the per-sensor option and if I find
        # something there, I replace - if was set from first step -  broker configs (or simply add a new entry)

        for optionToSearch in POSSIBLE_OPTIONS:
            # 1: Set from broker's configs
            if optionToSearch in self.brokerConfigs:
                self.options[optionToSearch] = self.brokerConfigs[optionToSearch]

            # 2: Set from sensor's configs
            if self.sensorConfigs and optionToSearch in self.sensorConfigs:
                self.options[optionToSearch] = self.sensorConfigs[optionToSearch]

    def GetOption(self, path,defaultReturnValue=None):
        return cf.GetOption(self.options,path,defaultReturnValue)
        
    def ListTopics(self):
        return self.topics

    def AddTopic(self, topic):
        self.addedTopics += 1

        # If user in options defined custom topics, store original and custom topic and replace it in the send function
        replaced = False
        if self.GetOption('custom_topics') is not None and len(self.GetOption('custom_topics')) >= self.addedTopics:
            self.replacedTopics.append(
                {'original': topic, 'custom': self.GetOption('custom_topics')[self.addedTopics-1]})
            self.Log(Logger.LOG_INFO, 'Using custom topic defined in options')
            replaced = True

        self.topics.append({'topic': topic, 'value': ""})

        self.Log(Logger.LOG_DEVELOPMENT,"Adding topic: " + topic)
        self.Log(Logger.LOG_DEVELOPMENT,"Discovery topic normalizer: " + topic.replace("/","_"))

    def GetFirstTopic(self):
        return self.topics[0]['topic'] if len(self.topics) else None

    def GetTopicByName(self, name):
        # Using topic string, I get his dict from topics list
        for topic in self.topics:
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
            self.Log(Logger.LOG_ERROR, Logger.ExceptionTracker.TrackString(exc))
            self.sensorManager.UnloadSensor(self.name, self.monitor_id)

    def Update(self):  # Implemented in sub-classes - Here values are taken
        self.Log(Logger.LOG_WARNING, 'Update method not implemented')
        pass  # Must not be called directly, cause stops everything in exception, call only using CallUpdate

    def SelectTopic(self,topic):
        # for a topic look for its customized topic and return it if there's. Else return the default one but completed with GetTopic 
        
        for customs in self.replacedTopics:
            # If it's in the list of topics to replace
            if topic['topic'] == customs['original']:
                return customs['custom']
        
        return self.GetTopic(topic['topic'])


    def SendData(self):
        if self.GetOption('dont_send') is True:
            return  # Don't send if disabled in config

        if self.mqtt_client is not None:
            for topic in self.topics:  # Send data for all topic

                # For each topic I check if I send to that or if it has to be replaced with a custom topic defined in options
                topicToUse = self.SelectTopic(topic)

                # Log the topic as debug if it's on
                if 'debug' in self.brokerConfigs and self.brokerConfigs['debug'] is True:
                    self.Log(Logger.LOG_DEBUG, "Sending data to " + topicToUse)

                self.mqtt_client.SendTopicData(
                    topicToUse, topic['value'])

    def FindCommand(self, name):  # Find active commands for some specific action
        if(self.sensorManager):
            if(self.sensorManager.commandManager):
                return self.sensorManager.commandManager.FindCommand(name, self.monitor_id)
            else:
                self.Log(Logger.LOG_ERROR,
                         'SensorManager not set in the CommandManager!')
        else:
            self.Log(Logger.LOG_ERROR,
                     'SensorManager not set in the sensor!')
        return None

    def FindSensor(self, name):  # Find active sensors for some specific action
        if(self.sensorManager):
            return self.sensorManager.FindSensor(name, self.monitor_id)
        else:
            self.Log(Logger.LOG_ERROR,
                     'SensorManager not set in the sensor!')
        return None

    def GetTopic(self, last_part_of_topic):
        model = TOPIC_FORMAT
        if 'topic_prefix' in self.brokerConfigs:
            model = self.brokerConfigs['topic_prefix'] + '/'+model
        return model.format(self.brokerConfigs['name'], last_part_of_topic)

    # Calculate if a send_interval spent since the last sending time
    def ShouldSendMessage(self):
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

    # Calculate if a send_interval spent since the last sending time
    def ShouldSendDiscoveryConfig(self):
        if self.GetLastDiscoveryTime() is None:  # Never sent anything
            return True  # Definitely yes, you should send
        else:
            # Calculate time elapsed
            # Get current time
            now = datetime.datetime.now()
            # Calculate
            seconds_elapsed = (now-self.GetLastDiscoveryTime()).total_seconds()
            # Check if now I have to send
            if seconds_elapsed >= self.GetSendDiscoveryConfigInterval():
                return True
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

    def GetSensorName(self):
        # Only SENSORCLASS (without Sensor suffix)
        return self.GetClassName().split('.')[-1].split('Sensor')[0]

    def GetSendMessageInterval(self):
        return self.send_interval

    def GetSendDiscoveryConfigInterval(self):
        # Search in config or use default
        return cf.GetOption(self.brokerConfigs,[DISCOVERY_KEY,DISCOVERY_PUBLISH_INTERVAL_KEY],DISCOVERY_PUBLISH_INTERVAL_DEFAULT)

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

    def LoadRequirements(self):
        # 1: Get path of the single object
        # 2: If I dont find the yaml in that folder, I return None
        # 3: If I find it, I parse the yaml and I return the dict
        # Start:
        # 1
        requirements_path = path.join(
            self.sensorPath, OBJECT_SETTINGS_FILENAME)
        # try 3 except 2
        try:
            with open(requirements_path) as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        except:
            return None



    def PublishDiscoveryData(self):
        payload = None

        # Check if Discovery is enabled
        if cf.GetOption(self.brokerConfigs,[DISCOVERY_KEY,DISCOVERY_ENABLE_KEY],False) is not False:
            # Okay need auto discovery
            
            # Not for don't send sensors
            if self.GetOption('dont_send') is True:
                return  # Don't send if disabled in config
            
            prefix = cf.GetOption(self.brokerConfigs,[DISCOVERY_KEY,DISCOVERY_DISCOVER_PREFIX_KEY],DISCOVERY_DISCOVER_PREFIX_DEFAULT) 

            for topic in self.topics:
                payload = {}
                # Check here if I have an entry in the discovery file for this topic and use that data (PLACE IN 'sensor_data')
                sensor_data = None # THIS

                # Do I have the type in the config or do I set it to 'sensor' ?
                if not sensor_data or not 'type' in sensor_data:
                    sensor_type="sensor"

                # Do I have the name in the config or do I set it using the default topic ?
                if not sensor_data or not 'name' in sensor_data:
                    payload['name'] = topic['topic'].replace("/","_")

                # Check and add this only if has option true
                if cf.GetOption(self.brokerConfigs,[DISCOVERY_KEY,DISCOVERY_NAME_PREFIX_KEY],DISCOVERY_NAME_PREFIX_DEFAULT):
                    payload['name'] = "Monitor " + self.brokerConfigs['name'] + " - " + payload['name']


                payload['state_topic']=self.SelectTopic(topic)

                topic_component=self.TopicRemoveBadCharacters(self.brokerConfigs['name']+"_"+topic['topic'])
                config_send_topic = AUTODISCOVERY_TOPIC_CONFIG_FORMAT.format(prefix,sensor_type,topic_component)
                
                self.mqtt_client.SendTopicData(
                        config_send_topic, json.dumps(payload))

            '''
        # Check if I have to reset Discovery (send blank payload)
        if cf.GetOption(self.brokerConfigs,[DISCOVERY_KEY,DISCOVERY_RESET_KEY],False) is not False:
                topic_component=self.TopicRemoveBadCharacters(self.brokerConfigs['name']+"_"+topic['topic'])
                config_send_topic = AUTODISCOVERY_TOPIC_CONFIG_FORMAT.format(prefix,sensor_type,topic_component)
                
                self.mqtt_client.SendTopicData(
                        config_send_topic, json.dumps(payload))
            '''


    def TopicRemoveBadCharacters(self, string):
        return string.replace("/","_").replace(" ","_").replace("-","_").lower()


    def Log(self, messageType, message):
        self.logger.Log(messageType, self.name+' Sensor', message)
