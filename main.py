import time
import os
import sys
import platform
import subprocess
import psutil
from time import strftime
import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

if len(sys.argv) < 5:
    print("You must pass broker address, client name, username and password")
    sys.exit()
broker = sys.argv[1]
name = sys.argv[2]

username = sys.argv[3]
password = sys.argv[4]

main_topic = "monitor/"+name+"/"
# Topic informazioni
ram_topic = main_topic+'ram_used_percentage'
cpu_topic = main_topic+'cpu_used_percentage'
disk_topic = main_topic+'disk_used_percentage'
os_topic = main_topic+'operating_system'
time_topic = main_topic+'message_time'
# Topic comandi
shutdown_topic = main_topic+"shutdown_command"
reboot_topic = main_topic+"reboot_command"
lock_topic = main_topic+"lock_command"

#Delay in second
message_send_delay = 10
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
    'Darwin': {
        'shutdown': 'sudo shutdown -h now',
        'reboot': 'sudo reboot',
        'lock': {
            'base': 'pmset displaysleepnow'
        }
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


def Get_RAM_Percentage():
    return psutil.virtual_memory()[2]


def Get_CPU_Percentage():
    return psutil.cpu_percent()


def Get_Disk_Used_Percentage():
    return psutil.disk_usage('/')[3]


def Get_Operating_System():
    return platform.system()


def Get_Desktop_Environment():
    de = os.environ.get('DESKTOP_SESSION')
    if de != None:
        return de
    else:
        return "base"


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
    # Quando ho la connessione mi iscrivo ai topic per ricevere i comandi
    # Inserisco qua le subscription per eseguirle anche al riavvio del server
    global client_connected
    if rc == 0:  # Se la connessione è riuscita
        print("Connection established")
        client_connected = True
        client.subscribe(shutdown_topic)
        client.subscribe(reboot_topic)
        client.subscribe(lock_topic)
    else:
        print("Can't connect")

def on_message(client, userdata, message):
    if message.topic == shutdown_topic:
        Shutdown()
    elif message.topic == reboot_topic:
        Reboot()
    elif message.topic == lock_topic:
        Lock()
    else:
        print("Unknown topic: " + message.topic)


def on_disconnect(client, userdata, rc):
    global client_connected
    print("Connection lost")
    client_connected = False


print("Broker: " + broker)
print("Topic: " + main_topic)
print("OS: " + Get_Operating_System())
print("Desktop Environment: " + Get_Desktop_Environment())
print("Message send every " + str(message_send_delay) + " seconds")


# Preparo il client
client = mqtt.Client("monitor-" + name)
client.username_pw_set(username,password)
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Mi connetto al server in modo asincrono:
# se il server non è raggiungibile, appena sarà possibile avverrà la connessione
client.connect_async(broker)

# Inizio il loop di invio dei dati ogni {delay} secondi
client.loop_start()

while True:
    if client_connected:
        # Invio la % della RAM usata
        client.publish(ram_topic, Get_RAM_Percentage())
        # Invio la % della CPU usata
        client.publish(cpu_topic, Get_CPU_Percentage())
        # Invio la % del disco usato
        client.publish(disk_topic, Get_Disk_Used_Percentage())
        # Invio il Sistema Operativo
        client.publish(os_topic, Get_Operating_System())
        # Invio l'ora attuale
        client.publish(time_topic, Get_Time())
    time.sleep(message_send_delay)
