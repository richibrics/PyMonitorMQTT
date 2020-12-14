# PyMonitorMQTT
PyMonitorMQTT is a **cross-platform system monitor** (works both on Windows, Linux and macOS) that sends real time information via **MQTT**.
The information is sent every 10 seconds and the broker can perform certain actions on the monitor's computer.

Information form this client are well managed by home automation systems like [HomeAssistant](https://github.com/home-assistant/home-assistant).
**Companion integration for HomeAssistant can be found [here](https://github.com/richibrics/HassMonitorMqtt)**

Available information:
* RAM in use (%)
* CPU in use (%)
* Hard Disk used space (%)
* CPU Temperature (°C)
* Battery Level (%)
* Charging status 
* Screenshot
* Timestamp of the data
* Running Operating System
* Brightness

Actions:
* Shutdown
* Reboot
* Lock
* Set Brightness

## Compatibility
The monitor works both on Windows, Linux and macOS

The battery sensor works only with battery-powered computers.

CPU Temperature works only on Linux and Windows (not in macOS).

Brightness sensor and command doesn't work on Linux yet.

Most commands require both the **OS** sensor and the **DesktopEnvironment** sensor **enabled** to ensure proper operation for the operating system and the desktop environment!

## Getting Started

These instructions will get you a copy of the project up and running on your local machine. See deployment for notes on how to deploy the project on a live system.

### Installing

#### Install Python

PyMonitorMQTT needs Python3.7 to run.
You can install it [here](https://www.python.org/downloads/).

#### Install PIP
To install required packages you need [pip](https://www.makeuseof.com/tag/install-pip-for-python/)

#### Dependencies
To install dependencies all together, you only have to type in your terminal
```
python3 -m pip install -r requirements.txt
```

In addition, to get CPU temperature from Windows you need:
* wmi (module from pip): `python3 -m pip install wmi`
* Open Hardware Monitor (external software). [Download it](https://openhardwaremonitor.org/downloads/)

## Running the script

To start the monitor you need to type the following command in the terminal:
```
python3 main.py
```

## Configure
To configure the montior client, you need to create a text file in the project folder named "configuration.yaml"

File example: (UPDATED IN WIKI)
```
monitors:
  - broker: example.com
    name: PC_NAME
    port: 1883
    username: example
    password: example
    send_interval: 20 # Seconds
    topic_prefix: example_prefix
    print_topics: False

    sensors:
      - Cpu
      - CpuTemperatures
      - Ram
      - Os
      - DesktopEnvironment:
          dont_send: True      
      - Battery
      - Disk
      - Time
      - Screenshot:
          custom_topic: shevchenko/photo
      - Brightness

    commands:
      - Lock
      - Reboot
      - Shutdown
      - Brightness

```

Schema:
* broker: {String} Address (IP or name) of MQTT broker **[COMPULSORY]**
* name: {String} Name of the client; will be part of sensors and commands topics **[COMPULSORY]**
* username: {String} Username to login with the broker **[OPTIONAL]**
* password: {String} Password to login with the broker **[OPTIONAL - COMPULSORY if username is set]** 
* topic_prefix: {String} Prefix to add at the start of each topic (e.g. example_prefix/monitor/PC_NAME/mysensor_topic) **[OPTIONAL]**
* print_topics: {Boolean} To discover all topics of the monitor **[OPTIONAL: default is False]**

* sensors: {List of strings} List of sensors to enable **[COMPULSORY]**
* commands: {List of strings} List of commands to enable **[COMPULSORY]**

Each sensor/command in the list sensors/commands list to enable, can have other options:
* custom_topic: {String} Use a custom topic for that sensor/command **[OPTIONAL]**
* dont_send: {Boolean} Prevents a sensor from sending information to the broker (only for sensors) **[OPTIONAL]**


## MQTT Topics
On the server you must specify sensors and commands topics

You can discover topics setting 'print_topics' as True in your configuration file
### Sensors
```
Sensor Topic: monitor/PC_NAME/SENSOR_SPECIFIC_TOPIC
```
where SENSOR_SPECIFIC_TOPIC can be found in Sensors/SensorName/SensorName.py: TOPIC variable
### Commands
```
Command Topic: monitor/PC_NAME/COMMAND_SPECIFIC_TOPIC
```
where COMMAND_SPECIFIC_TOPIC can be found in Commands/CommandName/CommandName.py: TOPIC variable
## HomeAssistant with PyMonitorMQTT example

![HomeAssistant Example](Home%20Assistant%20Monitors.png?raw=true "HomeAssistant Example")

## Authors

**Riccardo Briccola** - Project development - [Github Account](https://github.com/richibrics)
