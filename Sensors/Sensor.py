import datetime
from consts import *
import Logger
from ValueFormatter import ValueFormatter


class Sensor():
    # To replace an original topic with a personalized one from configuration (may not be used).
    # When a sensor send the data with a topic, if the user choose a fixed topic in config,
    # then when I send the data I don't use the topic defined in the function but I replaced that
    # with the user's one that I store in this list of dict
    lastSendingTime = None
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

    def GetOption(self, option):
        # if in options I have a value for that option rerturn that else return False
        if option in self.options:
            return self.options[option]
        else:
            return False

    def ListTopics(self):
        return self.topics

    def AddTopic(self, topic):
        self.addedTopics += 1

        # If user in options defined custom topics, store original and custom topic and replace it in the send function
        replaced = False
        if self.GetOption('custom_topics') is not False and len(self.GetOption('custom_topics')) >= self.addedTopics:
            self.replacedTopics.append(
                {'original': topic, 'custom': self.GetOption('custom_topics')[self.addedTopics-1]})
            self.Log(Logger.LOG_INFO, 'Using custom topic defined in options')
            replaced = True

        self.topics.append({'topic': topic, 'value': ""})

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

    def SendData(self):
        if self.GetOption('dont_send') is True:
            return  # Don't send if disabled in config

        if self.mqtt_client is not None:
            for topic in self.topics:  # Send data for all topic

                # For each topic I check if I send to that or if it has to be replaced with a custom topic defined in options
                topicToUse = self.GetTopic(topic['topic'])

                for customs in self.replacedTopics:
                    # If it's in the list of topics to replaced
                    if topic['topic'] == customs['original']:
                        topicToUse = customs['custom']

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
    def ShouldSend(self):
        if self.GetLastSendingTime() is None:  # Never sent anything
            return True  # Definitely yes, you should send
        else:
            # Calculate time elapsed
            # Get current time
            now = datetime.datetime.now()
            # Calculate
            seconds_elapsed = (now-self.GetLastSendingTime()).total_seconds()
            # Check if now I have to send
            if seconds_elapsed >= self.GetSendInterval():
                return True
            else:
                return False

    # Save the time when last message is sent. If no time passed, will be used current time
    def SaveTimeMessageSent(self, time=None):
        if time is not None:
            self.lastSendingTime = time
        else:
            self.lastSendingTime = datetime.datetime.now()

    def GetClassName(self):
        # Sensor.SENSORFOLDER.SENSORCLASS
        return self.__class__.__name__

    def GetSensorName(self):
        # Only SENSORCLASS (without Sensor suffix)
        return self.GetClassName().split('.')[-1].split('Sensor')[0]

    def GetSendInterval(self):
        return self.send_interval

    def GetMqttClient(self):
        return self.mqtt_client

    def GetLogger(self):
        return self.logger

    def GetMonitorID(self):
        return self.monitor_id

    def GetLastSendingTime(self):
        return self.lastSendingTime

    def Log(self, messageType, message):
        self.logger.Log(messageType, self.name+' Sensor', message)
