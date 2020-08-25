# PyMonitorMQTT
PyMonitorMQTT is an universal system monitor (works both on Windows, Linux and macOS) that sends real time information via MQTT to home automations systems like [HomeAssistant](https://github.com/home-assistant/home-assistant).
The information is sent every 10 seconds and the broker can perform certain actions on the monitor's computer.
Companion integration for HomeAssistant can be found [here](https://github.com/richibrics/HassMonitorMqtt)

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

Battery sensor works only with battery-powered computers.
CPU Temperature works only in Linux and Windows (not in macOS)
Brightness sensor and command doesn't work in Linux yet

## Getting Started

These instructions will get you a copy of the project up and running on your local machine. See deployment for notes on how to deploy the project on a live system.

### Installing

#### Install Python

PyMonitorMQTT needs Python3.7 to run.
You can install it [here](https://www.python.org/downloads/).

#### Install PIP
To install required packages you need [pip](https://www.makeuseof.com/tag/install-pip-for-python/). Once you installed it, type
```
python -m pip install [REQUIRED_MODULE]
```
to install the dependencies.

#### Dependencies
To install dependencies all together, you only have to type in your terminal
```
python -m pip install -r requirements.txt
```

In addition, to get CPU temperature from Windows you need:
* wmi (module from pip) - should already be in requirements.txt file
* Open Hardware Monitor (external software). [Download it](https://openhardwaremonitor.org/downloads/)

## Running the script

To start the monitor you need to type the following command in the terminal:
```
python main.py
```

## Configure
To configure the montior client, you need to create a text file in the project folder named "configuration.yaml"

File example:
```
broker: BROKER_ADDRESS
name: PC_NAME
update_rate: 20 # Seconds

sensors:
  - Cpu
  - CpuTemperatures
  - Ram
  - Os
  - DesktopEnvironment
  - Battery
  - Disk
  - Time
  - Screenshot
  - Brightness

commands:
  - Lock
  - Reboot
  - Shutdown
  - Brightness

```



## MQTT Topics
On the server you must specify sensors and commands topics
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
