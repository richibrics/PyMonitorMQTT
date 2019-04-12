# PyMonitorMQTT
PyMonitorMQTT is an universal system monitor (works both on Windows, Linux and macOS) that sends real time information via MQTT to hubs like [HomeAssistant](https://github.com/home-assistant/home-assistant).
The information is sent every 10 seconds and the broker can perform certain actions on the monitor's computer.

Available information:
* RAM in use (%)
* CPU in use (%)
* Hard Disk used space (%)
* Running Operating System
* Information time

Actions:
* Shutdown
* Reboot
* Lock

## Getting Started

These instructions will get you a copy of the project up and running on your local machine. See deployment for notes on how to deploy the project on a live system.

### Installing

PyMonitorMQTT needs Python3.7 to run.
You can install it [here](https://www.python.org/downloads/).
Then you need to install these dependencies:
* paho-mqtt
* psutil

To install these packages you need [pip](https://www.makeuseof.com/tag/install-pip-for-python/). Once you installed it type
```
python -m pip install paho-mqtt psutil
```
If it has been successful you are ready to run PyMonitorMQTT!

## Running the script

To start the monitor you need to type the following command in the terminal:
```
python main.py BROKER PC_NAME
```
where
* **BROKER** must be replaced with the broker (MQTT server) address (hostname or ip)
* **PC_NAME** must be replaced with a custom name for your comuputer. This is necessary to recognise monitor's information on the server.

### Topics
On the server you must specify information and actions topics:
* RAM in use (%): monitor/PC_NAME/ram_used_percentage
* CPU in use (%): monitor/PC_NAME/cpu_used_percentage
* Hard Disk used space (%):  monitor/PC_NAME/disk_used_percentage
* Running Operating System:  monitor/PC_NAME/operating_system
* Information time:  monitor/PC_NAME/message_time
* Shutdown action: monitor/PC_NAME/shutdown_command
* Reboot action: monitor/PC_NAME/reboot_command
* Lock action: monitor/PC_NAME/lock_command

## Authors

**Riccardo Briccola** - Project development - [Github Account](https://github.com/richibrics)
