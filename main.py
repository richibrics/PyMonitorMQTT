import time
import random
import psutil
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


def Get_RAM_Percentage():
    return psutil.virtual_memory()[2]


def Get_CPU_Percentage():
    return psutil.cpu_percent()


broker = '192.168.1.214'
main_topic = "monitor/pc-di-riccardo/"
ram_topic = main_topic+'ram_percentage'
cpu_topic = main_topic+'cpu_percentage'
shutdown_topic = main_topic+"shutdown"
delay = 5
#Preparo il client
client = mqtt.Client("monitor_pc-di-riccardo")
#Mi connetto al server
client.connect(broker)
#Mi iscrivo al topic per i comandi
client.subscribe(shutdown_topic)
#Inizio il loop di invio dei dati ogni {delay} secondi
client.loop_start()
while True:
    #Invio la % della RAM usata
    client.publish(ram_topic, Get_RAM_Percentage())
    #Invio la % della CPU usata
    client.publish(cpu_topic, Get_CPU_Percentage())
    time.sleep(delay)
