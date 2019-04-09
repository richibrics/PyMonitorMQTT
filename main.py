import time
import sys
import platform
import subprocess
import random
import psutil
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


def Get_RAM_Percentage():
    return psutil.virtual_memory()[2]


def Get_CPU_Percentage():
    return psutil.cpu_percent()


def Get_Disk_Used_Percentage():
    return psutil.disk_usage('/')[3]


def Get_Operating_System():
    return platform.system()


def Shutdown():
    print("I am going to shutdown the computer")
    if Get_Operating_System() == 'Windows':
        cmdCommand = "shutdown -s"
        subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
    else:
        cmdCommand = "sudo shutdown -h now"
        subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)


def Reboot():
    print("I am going to reboot the computer")
    if Get_Operating_System() == 'Windows':
        cmdCommand = "shutdown -r"
        subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
    else:
        cmdCommand = "sudo reboot"
        subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)


def Lock():
    print("I am going to lock the computer")
    if Get_Operating_System() == 'Windows':
        cmdCommand = "rundll32.exe user32.dll,LockWorkStation"
        subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
    elif Get_Operating_System() == 'Darwin':  # MacOS command
        cmdCommand = "pmset displaysleepnow"
        subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
    else:
        cmdCommand = "sudo vlock -a"
        subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)


def on_message(client, userdata, message):
    if message.topic == shutdown_topic:
        Shutdown()
    elif message.topic == reboot_topic:
        Reboot()
    elif message.topic == lock_topic:
        Lock()
    else:
        print("Unknown topic: " + message.topic)


def on_connect(client, userdata, flags, rc):
    # Quando ho la connessione mi iscrivo ai topic per ricevere i comandi
    # Inserire qua le subscription per eseguirle anche al riavvio del server
    client.subscribe(shutdown_topic)
    client.subscribe(reboot_topic)
    client.subscribe(lock_topic)


if len(sys.argv) < 3:
    sys.exit()
broker = sys.argv[1]
name = sys.argv[2]
main_topic = "monitor/"+name+"/"
print("Broker: " + broker)
print("Topic: " + main_topic)

# Topic informazioni
ram_topic = main_topic+'ram_used_percentage'
cpu_topic = main_topic+'cpu_used_percentage'
disk_topic = main_topic+'disk_used_percentage'
os_topic = main_topic+'operating_system'
# Topic comandi
shutdown_topic = main_topic+"shutdown_command"
reboot_topic = main_topic+"reboot_command"
lock_topic = main_topic+"lock_command"

delay = 10
# Preparo il client
client = mqtt.Client("monitor-" + name)
client.on_message = on_message
client.on_connect = on_connect
# Mi connetto al server
client.connect(broker)
# Inizio il loop di invio dei dati ogni {delay} secondi
client.loop_start()

while True:
    # Invio la % della RAM usata
    client.publish(ram_topic, Get_RAM_Percentage())
    # Invio la % della CPU usata
    client.publish(cpu_topic, Get_CPU_Percentage())
    # Invio la % del disco usato
    client.publish(disk_topic, Get_Disk_Used_Percentage())
    # Invio il Sistema Operativo
    client.publish(os_topic, Get_Operating_System())
    time.sleep(delay)
