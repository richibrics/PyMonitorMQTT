# PyMonitorMQTT
PyMonitorMQTT is an universal system monitor (works both on Windows, Linux and macOS) that sends real time information via MQTT to home automations systems like [HomeAssistant](https://github.com/home-assistant/home-assistant).
The information is sent every 10 seconds and the broker can perform certain actions on the monitor's computer.

Available information:
* RAM in use (%)
* CPU in use (%)
* Hard Disk used space (%)
* CPU Temperature (°C)
* Battery Level (%)
* Charging status 
* Timestamp of the data
* Running Operating System

Actions:
* Shutdown
* Reboot
* Lock

## Compatibility

Battery sensor works only with battery-powered computers.
CPU Temperature works only in Linux and Windows (not in macOS)

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
Then you need to install these dependencies:
* paho-mqtt (module from pip)
* psutil (module from pip)

In addition, to get CPU temperature from Windows you need:
* wmi (module from pip)
* Open Hardware Monitor (external software). [Download it](https://openhardwaremonitor.org/downloads/)

## Running the script

To start the monitor you need to type the following command in the terminal:
```
python main.py -b BROKER -n PC_NAME
```
where
* **BROKER** must be replaced with the broker (MQTT server) address (hostname or ip)
* **PC_NAME** must be replaced with a custom name for your computer. This is necessary to recognise monitor's information on the server.

### Help page
```
usage: main.py [-h] -b BROKER -n NAME [-u USERNAME] [-p PASSWORD]
               [-de DESKTOP_ENVIRONMENT]

required arguments:
  -b BROKER, --broker BROKER
                        MQTT Broker
  -n NAME, --name NAME  Client name

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Broker username (default set to ""
  -p PASSWORD, --password PASSWORD
                        Broker password (default set to ""
  -de DESKTOP_ENVIRONMENT, --desktop-environment DESKTOP_ENVIRONMENT
                        Desktop environment (to use if it's wrongly detected)
```

## MQTT Topics
On the server you must specify sensors and commands topics
### Sensors
```
- RAM in use (%): monitor/PC_NAME/ram_used_percentage
- CPU in use (%): monitor/PC_NAME/cpu_used_percentage
- Hard Disk used space (%):  monitor/PC_NAME/disk_used_percentage
- CPU temperature (°C):  monitor/PC_NAME/cpu_temperature
- Battery level (%):  monitor/PC_NAME/battery_level_percentage
- Battery charging status:  monitor/PC_NAME/battery_charging
- Running operating system:  monitor/PC_NAME/operating_system
- Information time:  monitor/PC_NAME/message_time
```
### Commands
```
- Shutdown action: monitor/PC_NAME/shutdown_command
- Reboot action: monitor/PC_NAME/reboot_command
- Lock action: monitor/PC_NAME/lock_command
```

## HomeAssistant with PyMonitorMQTT example

![HomeAssistant Example](Home%20Assistant%20Monitors.png?raw=true "HomeAssistant Example")

## Authors

**Riccardo Briccola** - Project development - [Github Account](https://github.com/richibrics)
