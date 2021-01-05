# PyMonitorMQTT

{% for page in site.pages %}
    <a href={{ page.path }}>{{ page.title }}</a>
{% endfor %}


{% for file in site.static_files %}
    <a href={{ file.path }}>a</a>
{% endfor %}


{% for item in site.pages %}
    {% if item.title != null %}
        <a class="sidebar-nav-item{% if item.url == page.url %} active{% endif %}" href="{{ site.baseurl }}{{ item.url  | remove_first: '/' }}">{{ item.title }}</a>
    {% endif %}
{% endfor %}


## About the application
PyMonitorMQTT is a **cross-platform system monitor** (works both on Windows, Linux and macOS) that sends real time information via **MQTT**.
The information is sent periodically and the broker can perform certain actions on the monitor's computer.

The specialty of script is the high level of customization: for example you can add as much brokers as you want, choose the data send interval, which sensors and commands to enable, on which custom topic, and so much more !

Information form this client are well managed by home automation systems like [HomeAssistant](https://github.com/home-assistant/home-assistant).
**Companion integration for HomeAssistant can be found [here](https://github.com/richibrics/HassMonitorMqtt)**

## Why you should use it
Many home automation systems support MQTT so in no time you can connect the monitor and receive the data.

You can choose which information you want to send, to which topic and which not.

You can automate scripts to run when a topic message is received (with the Terminal command) and report the output to a file which content will be sent as a message (with the File sensor).

**Soon** will be available a Serial sensor to report via MQTT the status of a Serial device connected to the computer and a Serial command to communicate with the device and trigger some actions. Possible uses:
* Receive via Serial USB the room temperature via thermometer
* Get Relay status (open/close)
* Trigger Relay to power on/off lights/air conditioners/...
* many other purposes !
Best to be used with Arduino and microcontrollers.

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
