import time
import sys
import platform
import subprocess
import psutil
from time import strftime
import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

if len(sys.argv) < 3:
    print("You must pass broker address and client name")
    sys.exit()
broker = sys.argv[1]
name = sys.argv[2]

main_topic = "monitor/"+name+"/"
# Topic informazioni
status_topic = main_topic+'status'
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
connection_error_delay = 5
client_connected = False
connection_failed = False


def Get_RAM_Percentage():
    return psutil.virtual_memory()[2]


def Get_CPU_Percentage():
    return psutil.cpu_percent()


def Get_Disk_Used_Percentage():
    return psutil.disk_usage('/')[3]


def Get_Operating_System():
    return platform.system()


def Get_Desktop_Enviroment():
    return os.environ.get('DESKTOP_SESSION')


def Get_Time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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
    if Get_Operating_System() == 'Windows': #Windows command
        cmdCommand = "rundll32.exe user32.dll,LockWorkStation"
        subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
    elif Get_Operating_System() == 'Darwin':  # MacOS command
        cmdCommand = "pmset displaysleepnow"
        subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
    elif Get_Operating_System() == 'Linux':  #Linux command
        if Get_Desktop_Enviroment() == "cinnamon":
            cmdCommand = "cinnamon-screensaver-command -a"
            subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
        elif Get_Desktop_Enviroment() == "gnome":
            cmdCommand = "gnome-screensaver-command -l"
            subprocess.Popen(cmdCommand.split(), stdout=subprocess.PIPE)
        else:
            print("Desktop Enviroment non riconosciuto, segnala su https://github.com/richibrics/PyMonitorMQTT/issues")

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

# Preparo il client
client = mqtt.Client("monitor-" + name)
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
        # Invio lo stato
        client.publish(status_topic, "home")
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
        print(Get_Time())
    time.sleep(message_send_delay)
