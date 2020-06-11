import os
import time
import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import yaml
import argparse
import Sensors
import Managers

sensorManager = None
config = None
config_filename = 'configuration.yaml'

scriptFolder = str(os.path.dirname(os.path.realpath(__file__)))

# Delay in second
message_send_delay = 20
not_connected_delay = 1

client_connected = False
connection_failed = False


def on_connect(client, userdata, flags, rc):
    # Subscribe to thetopics to receive action command when connection is set
    # Will subscribe also if server reboots
    global client_connected
    if rc == 0:  # Connections is OK
        print("Connection established")
        client_connected = True
    else:
        print("Can't connect")


def on_disconnect(client, userdata, rc):
    global client_connected
    print("Connection lost")
    client_connected = False


def on_message(client, userdata, message):
    pass


def ParseArguments():
    # Parse arguments
    global args

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--broker', dest='broker', type=str, required=True,
                        help="MQTT Broker")
    parser.add_argument('-n', '--name', dest='name', type=str, required=True,
                        help="Client name")
    parser.add_argument('-u', '--username', dest='username', type=str, default='', required=False,
                        help='Broker username (default set to ""')
    parser.add_argument('-p', '--password', dest='password', type=str, default='', required=False,
                        help='Broker password (default set to ""')
    parser.add_argument('-de', '--desktop-environment', dest='desktop_environment', type=str, default=None, required=False,
                        help='Desktop environment (to use if it\'s wrongly detected)')
    args, unknown = parser.parse_known_args()


def Main():
    LoadYAML()
    # Prepare client
    client = mqtt.Client(config['name'])
    if 'username' in config and 'password' in config:
        client.username_pw_set(config['username'], config['password'])
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    sensorManager = Managers.SensorManager(config, client)

    # Connect async to the broker
    # If broker is not reachable, wait till he's reachable
    client.connect_async(config['broker'])

    # Send data in this loop every {delay} seconds
    client.loop_start()

    while True:
        if client_connected:
            # Update sensors and send data
            sensorManager.UpdateSensors()
            sensorManager.SendSensorsData()

            # Send sensros data
            time.sleep(message_send_delay)
        else:
            time.sleep(not_connected_delay)


def LoadYAML():
    global config
    with open(os.path.join(scriptFolder, config_filename)) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)


Main()
