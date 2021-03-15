import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from Logger import Logger, ExceptionTracker


class MqttClient():
    client = None
    connected = False

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        # Topics to subscribe, dict 'topic', Command (as 'callback')
        self.topics = []
        self.subscribed_topics = []  # Topics already subscribed
        # Prepare the client
        self.Log(Logger.LOG_INFO, 'Preparing MQTT client')
        self.SetupClient()
        self.AsyncConnect()
        self.Log(Logger.LOG_INFO, 'MQTT Client ready to connect')

    # SETUP PART

    def AsyncConnect(self):
        # Connect async to the broker
        # If broker is not reachable, wait till he's reachable
        if 'port' in self.config:
            self.client.connect_async(
                self.config['broker'], port=self.config['port'])
        else:
            self.client.connect_async(self.config['broker'])
        # Client ready to start -> activate callback
        self.client.loop_start()

    def SetupClient(self):
        if 'mqtt_id' in self.config:
            self.client = mqtt.Client(self.config['mqtt_id'])
        else:
            self.client = mqtt.Client(self.config['name'])

        if 'username' in self.config and 'password' in self.config:
            self.client.username_pw_set(
                self.config['username'], self.config['password'])

        # Assign event callbacks
        self.client.on_connect = self.Event_OnClientConnect
        self.client.on_disconnect = self.Event_OnClientDisconnect
        self.client.on_message = self.Event_OnMessageReceive

    # INCOMING MESSAGES PART

    def SendTopicData(self, topic, data):
        self.client.publish(topic, data)

    # OUTCOMING MESSAGES PART

    def AddNewTopic(self, topic, callbackCommand):
        self.topics.append({'topic': topic, 'callback': callbackCommand})
        self.SubscribeToTopic(topic)

    def SubscribeToTopic(self, topic):
        if topic not in self.subscribed_topics and self.connected:
            self.subscribed_topics.append(topic)
            self.client.subscribe(topic, 0)

    def UnsubscribeToTopic(self,topic):
        # Look for the topic in the list of tuples
        #for _tuple in self.subscribed_topics:
            #if _tuple[]

        if topic in self.subscribed_topics:
            for top in self.topics:
                if top['topic']==topic:        
                    self.topics.remove(top)
            self.subscribed_topics.remove(topic)
            self.client.unsubscribe(topic)
        

    def SubscribeToAllTopics(self):
        for topic in self.topics:
            self.SubscribeToTopic(topic['topic'])

    # EVENTS

    def Event_OnClientConnect(self, client, userdata, flags, rc):
        if rc == 0:  # Connections is OK
            self.Log(Logger.LOG_INFO, "Connection established")
            self.connected = True
            self.SubscribeToAllTopics()
        else:
            self.Log(Logger.LOG_ERROR, "Connection error")

    def Event_OnClientDisconnect(self, client, userdata, rc):
        self.Log(Logger.LOG_ERROR, "Connection lost")
        self.connected = False
        self.subscribed_topics.clear()

    def Event_OnMessageReceive(self, client, userdata, message):
        # Compare message topic whith topics in my list
        for topic in self.topics:
            if self.TopicArrivedMatches(message, topic):
                # Run the callback function of the Command assigned to the topic
                topic['callback'].CallCallback(message)

    # Check if topic of the message that just arrived is the same with the one I'm checking.
    # Some subscription (that end with #) receive messages from topics that start only in the same way but the end is different
    # (it's like the * wildcard) then I have to match also them
    def TopicArrivedMatches(self, message, topic):
        if message.topic == topic['topic']:
            return True
        if topic['topic'].endswith('#'):
            if topic['topic'] == '#':
                return True
            # Cut the # and check if message topic starts with my topic without #
            myTopic = topic['topic'][:-1]
            if message.topic.startswith(myTopic):
                return True

        return False

    def Log(self, messageType, message):
        self.logger.Log(messageType, 'MQTT', message)
