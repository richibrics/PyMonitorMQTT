import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import Logger


class MqttClient():
    client = None
    connected = False

    topics = []  # Topics to subscribe, dict 'topic', 'command'
    subscribed_topics = []  # Topics already subscribed

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        # Prepare the client
        self.Log(Logger.LOG_INFO, 'Preparing MQTT client')
        self.SetupClient()
        self.AsyncConnect()
        self.Log(Logger.LOG_INFO, 'MQTT Client ready')

    # SETUP PART

    def AsyncConnect(self):
        # Connect async to the broker
        # If broker is not reachable, wait till he's reachable
        self.client.connect_async(self.config['broker'])
        # Client ready to start -> activate callback
        self.client.loop_start()

    def SetupClient(self):
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
            print("Can't connect")

    def Event_OnClientDisconnect(self, client, userdata, rc):
        self.Log(Logger.LOG_ERROR, "Connection lost")
        self.connected = False
        self.subscribed_topics.clear()

    def Event_OnMessageReceive(self, client, userdata, message):
        # Compare message topic whith topics in my list
        for topic in self.topics:
            if message.topic == topic['topic']:
                # Run the callback function of the Command assigned to the topic
                topic['callback'].CallCallback(message)

    def Log(self, messageType, message):
        self.logger.Log(messageType, 'MQTT', message)
