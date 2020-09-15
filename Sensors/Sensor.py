from consts import *
import Logger


class Sensor():
    # To replace an original topic with a personalized one from configuration (may not be used).
    # When a sensor send the data with a topic, if the user choose a fixed topic in config,
    # then when I send the data I don't use the topic defined in the function but I replaced that
    # with the user's one that I store in this list of dict
    replacedTopics = []

    def __init__(self,  sensorManager, options, logger):  # Config is args
        self.topics = []  # List of {topic, value}
        self.sensorManager = sensorManager
        self.name = self.GetSensorName()
        self.options = options
        self.logger = logger
        self.addedTopics = 0
        # Do per sensor operations
        self.Initialize()

    def Initialize(self):  # Implemented in sub-classes
        pass

    def PostInitialize(self):  # Implemented in sub-classes
        pass

    def ListTopics(self):
        return self.topics

    def AddTopic(self, topic):
        self.addedTopics += 1

        # If user in options defined custom topics, store original and custom topic and replace it in the send function
        replaced = False
        if self.options and 'custom_topics' in self.options and len(self.options['custom_topics']) >= self.addedTopics:
            self.replacedTopics.append(
                {'original': topic, 'custom': self.options['custom_topics'][self.addedTopics-1]})
            self.Log(Logger.LOG_INFO, 'Using custom topic defined in options')
            replaced = True

        self.topics.append({'topic': topic, 'value': ""})

    def GetFirstTopic(self):
        return self.topics[0]['topic'] if len(self.topics) else None

    def GetTopicByName(self, name):
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

    def SetTopicValue(self, topic_name, value):
        topic = self.GetTopicByName(topic_name)
        if topic:
            topic['value'] = value
        else:
            self.Log(Logger.LOG_ERROR, 'Topic ' +
                     topic_name + ' does not exist !')

    def CallUpdate(self):  # Call the Update method safely
        try:
            self.Update()
        except Exception as exc:
            self.Log(Logger.LOG_ERROR, 'Error occured during update: '+str(exc))
            self.sensorManager.UnloadSensor(self.name)

    def Update(self):  # Implemented in sub-classes - Here values are taken
        self.Log(Logger.LOG_WARNING, 'Update method not implemented')
        pass  # Must not be called directly, cause stops everything in exception, call only using CallUpdate

    def SendData(self):
        if self.options and 'dont_send' in self.options and self.options['dont_send'] is True:
            return  # Don't send if disabled in config

        if self.sensorManager.mqttClient is not None:
            for topic in self.topics:  # Send data for all topic

                # For each topic I check if I send to that or if it has to be replaced with a custom topic defined in options
                topicToUse = self.GetTopic(topic['topic'])

                for customs in self.replacedTopics:
                    # If it's in the list of topics to replaced
                    if topic['topic'] == customs['original']:
                        topicToUse = customs['custom']

                # Log the topic as debug if it's on
                if 'debug' in self.sensorManager.config and self.sensorManager.config['debug'] is True:
                    self.Log(Logger.LOG_DEBUG, "Sending data to " + topicToUse)

                self.sensorManager.mqttClient.SendTopicData(
                    topicToUse, topic['value'])

    def GetTopic(self, last_part_of_topic):
        model = TOPIC_FORMAT
        if 'topic_prefix' in self.sensorManager.config:
            model = self.sensorManager.config['topic_prefix'] + '/'+model
        return model.format(self.sensorManager.config['name'], last_part_of_topic)

    def GetClassName(self):
        # Sensor.SENSORFOLDER.SENSORCLASS
        return self.__class__.__name__

    def GetSensorName(self):
        # Only SENSORCLASS (without Sensor suffix)
        return self.GetClassName().split('.')[-1].split('Sensor')[0]

    def Log(self, messageType, message):
        self.logger.Log(messageType, self.name+' Sensor', message)
