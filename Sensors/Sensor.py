from consts import *


class Sensor():

    def __init__(self, sensorManager):  # Config is args
        self.topics = []  # List of {topic, value}
        self.sensorManager = sensorManager
        self.name = self.GetSensorName()
        self.Initialize()

    def Initialize(self):  # Implemented in sub-classes
        pass

    def ListTopics(self):
        return self.topics

    def AddTopic(self, topic):
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
            print('Topic', topic_name, 'does not exist !')

    def CallUpdate(self):  # Call the Update method safely
        try:
            self.Update()
        except Exception as exc:
            print('Error during', self.name, 'update')
            print("Exception:", str(exc))
            self.sensorManager.UnloadSensor(self.name)

    def Update(self):  # Implemented in sub-classes - Here values are taken
        print('Update method not implemented')
        pass  # Must not be called directly, cause stops everything in exception, call only using CallUpdate

    def SendData(self):
        if self.sensorManager.mqttClient is not None:
            for topic in self.topics:
                self.sensorManager.mqttClient.SendTopicData(self.GetTopic(
                    topic['topic']), topic['value'])

    def GetTopic(self, last_part_of_topic):
        return TOPIC_FORMAT.format(self.sensorManager.config['name'], last_part_of_topic)

    def GetClassName(self):
        # Sensor.SENSORFOLDER.SENSORCLASS
        return self.__class__.__name__

    def GetSensorName(self):
        # Only SENSORCLASS (without Sensor suffix)
        return self.GetClassName().split('.')[-1].split('Sensor')[0]
