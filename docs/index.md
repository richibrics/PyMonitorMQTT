# PyMontitorMQTT

* TOC {:toc}

## About the application
PyMonitorMQTT is a **cross-platform system monitor** (works both on Windows, Linux and macOS) that sends real time information via **MQTT**.
The information is sent every 10 seconds and the broker can perform certain actions on the monitor's computer.

Information form this client are well managed by home automation systems like [HomeAssistant](https://github.com/home-assistant/home-assistant).
**Companion integration for HomeAssistant can be found [here](https://github.com/richibrics/HassMonitorMqtt)**

## Compatibility

PyMonitorMQTT just needs Python 3.7 and some pip modules to work. What are you waiting for ? These requirements are available on all possible operating systems and architectures.

Supported operating system:

* Windows 7/8/8.1/10 on Laptops/Desktops/2-in-1
* Linux 
* macOS
* Darwin
* Raspbian

Linux architectures:

* armhf
* arm64
* i386
* amd64
* x32
* x64

**Note**: some sensors and commands are not available for all the operating systems.
