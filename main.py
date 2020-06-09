import time
import os
import sys
import base64
import platform
import pyscreenshot as ImageGrab
from PIL import Image
import json
import subprocess
import psutil
from time import strftime
import re
import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import argparse

supports_win_temperature = True
try:
    import wmi  # Only to get windows temperature
    openhardwaremonitor = wmi.WMI(namespace="root\\OpenHardwareMonitor")
except:
    supports_win_temperature = False

topics = {'ram': 'ram_used_percentage',
          'cpu': 'cpu_used_percentage',
          'disk': 'disk_used_percentage',
          'os': 'operating_system',
          'time': 'message_time',
          'temperatures': 'cpu_temperature',
          'battery_level': 'battery_level_percentage',
          'battery_charging': 'battery_charging',
          'screenshot': 'screenshot',
          'shutdown': 'shutdown_command',
          'reboot': 'reboot_command',
          'lock': 'lock_command'}


# Delay in second
message_send_delay = 20
not_connected_delay = 1

scriptFolder = str(os.path.dirname(os.path.realpath(__file__)))

client_connected = False
connection_failed = False

commands = {
    'Windows': {
        'shutdown': 'shutdown /s',
        'reboot': 'shutdown /r',
        'lock': {
            'base': 'rundll32.exe user32.dll,LockWorkStation'
        }
    },
    'macOS': {
        'shutdown': 'sudo shutdown -h now',
        'reboot': 'sudo reboot',
        'lock': {
            'base': 'pmset displaysleepnow'
        },
        'temperature': 'sudo powermetrics -n 1'
    },
    'Linux': {
        'shutdown': 'sudo shutdown -h now',
        'reboot': 'sudo reboot',
        'lock': {
            'gnome': 'gnome-screensaver-command -l',
            'cinnamon': 'cinnamon-screensaver-command -a',
            'i3': 'i3lock'
        }
    }
}

def Take_Screenshot():
    filename=scriptFolder+'.screenshot.png'
    ImageGrab.grab().save(filename)
    f=open(filename, "rb") #3.7kiB in same folder
    fileContent = f.read()
    image = bytearray(fileContent)
    os.remove(filename)
    return image


def Get_RAM_Percentage():
    return psutil.virtual_memory()[2]


def Get_CPU_Percentage():
    return psutil.cpu_percent()


def Get_Disk_Used_Percentage():
    return psutil.disk_usage('/')[3]


def Get_Operating_System():
    os = platform.system()
    if os == 'Darwin':  # It's macOS
        return 'macOS'
    return os


def Get_Battery():
    battery = psutil.sensors_battery()
    if battery:  # Then the device has a battery
        return {'level': battery.percent, 'charging': battery.power_plugged}
    else:
        return {'level': 'None', 'charging': 'None'}


def Get_Desktop_Environment():
    if not args.desktop_environment:
        de = os.environ.get('DESKTOP_SESSION')
        if de != None:
            return de
        else:
            return "base"
    else:
        return args.desktop_environment


def Get_Temperatures():
    if(Get_Operating_System() == 'Windows'):
        return Get_Temperatures_Win()
    # elif(Get_Operating_System() == 'macOS'):
    #    return Get_Temperatures_macOS() NOT SUPPORTED
    elif(Get_Operating_System() == 'Linux'):
        return Get_Temperatures_Unix()


def Get_Temperatures_Unix():
    cpu_temps = []
    temps = psutil.sensors_temperatures()['coretemp']
    for temp in temps:
        if 'Core' in temp.label:
            cpu_temps.append(temp.current)
    # Send the list as json
    return str(json.dumps(cpu_temps))


# def Get_Temperatures_macOS():
    #command = commands['macOS']['temperature'] + ' | grep \'temperature\''
    # print(command)
    # out = subprocess.Popen(command.split(),
    #                       stdout=subprocess.PIPE,
    #                       stderr=subprocess.STDOUT)
    #out, errors = out.communicate()
    # from out, I have to get the float with temperature
    #temperature = [re.findall("\d+\.\d+", str(out))]
    # print(temperature)
    # Send the list as json
    # return str(json.dumps(temperature))


def Get_Temperatures_Win():
    if supports_win_temperature:
        # Needs OpenHardwareMonitor interface for WMI
        sensors = openhardwaremonitor.Sensor()
        cpu_temps = []
        for sensor in sensors:
            if sensor.SensorType == u'Temperature' and not 'GPU' in sensor.Name:
                cpu_temps += [float(sensor.Value)]
        cpu_temps.pop()  # Cause last temp is the highest value (summary)
        # Send the list as json
        return str(json.dumps(cpu_temps))
    return 'None'


def Get_Time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def Shutdown():
    print("I am going to shutdown the computer")
    command = commands[Get_Operating_System()]['shutdown']
    subprocess.Popen(command.split(), stdout=subprocess.PIPE)


def Reboot():
    print("I am going to reboot the computer")
    command = commands[Get_Operating_System()]['reboot']
    subprocess.Popen(command.split(), stdout=subprocess.PIPE)


def Lock():
    print("I am going to lock the computer")
    command = commands[Get_Operating_System(
    )]['lock'][Get_Desktop_Environment()]
    subprocess.Popen(command.split(), stdout=subprocess.PIPE)


def on_connect(client, userdata, flags, rc):
    # Subscribe to thetopics to receive action command when connection is set
    # Will subscribe also if server reboots
    global client_connected
    if rc == 0:  # Connections is OK
        print("Connection established")
        client_connected = True
        client.subscribe(GetTopic('shutdown'))
        client.subscribe(GetTopic('reboot'))
        client.subscribe(GetTopic('lock'))
    else:
        print("Can't connect")


def on_message(client, userdata, message):
    if message.topic == GetTopic('shutdown'):
        Shutdown()
    elif message.topic == GetTopic('reboot'):
        Reboot()
    elif message.topic == GetTopic('lock'):
        Lock()
    else:
        print("Unknown topic: " + message.topic)


def on_disconnect(client, userdata, rc):
    global client_connected
    print("Connection lost")
    client_connected = False


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


def GetTopic(name):
    main_topic = "monitor/" + args.name + "/"
    if name in topics:
        return main_topic + topics[name]
    else:
        return


def Main():
    ParseArguments()
    print("Broker: " + args.broker)
    print("OS: " + Get_Operating_System())
    print("Desktop Environment: " + Get_Desktop_Environment())
    print("Message send every " + str(message_send_delay) + " seconds")

    # Prepare client
    client = mqtt.Client("monitor-" + args.name)
    client.username_pw_set(args.username, args.password)
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    # Connect async to the broker
    # If broker is not reachable, wait till he's reachable
    client.connect_async(args.broker)

    # Send data in this loop every {delay} seconds
    client.loop_start()

    while True:
        if client_connected:
            # Send used RAM
            client.publish(GetTopic('ram'), Get_RAM_Percentage())
            # Send used CPU
            client.publish(GetTopic('cpu'), Get_CPU_Percentage())
            # Send used disk
            client.publish(GetTopic('disk'), Get_Disk_Used_Percentage())
            # Send OS
            client.publish(GetTopic('os'), Get_Operating_System())
            # Send current time
            client.publish(GetTopic('time'), Get_Time())
            # Send battery states
            battery_status = Get_Battery()
            client.publish(GetTopic('battery_level'), battery_status['level'])
            client.publish(GetTopic('battery_charging'),
                           str(battery_status['charging']))
            # Send cores temperatues
            client.publish(GetTopic('temperatures'), Get_Temperatures())
            client.publish(GetTopic('screenshot'), Take_Screenshot())

            time.sleep(message_send_delay)
        else:
            time.sleep(not_connected_delay)

Main()
