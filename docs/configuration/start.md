To configure the monitor client, you need to create a text file in the monitor folder named "configuration.yaml"

This file is written in YAML syntax. If you don't know how to make it work, [read this](https://rollout.io/blog/yaml-tutorial-everything-you-need-get-started/).

# Main configuration

PyMonitorMQTT supports more than one broker connection simultaneously. Each monitor configuration must be placed in the 'monitors' key that will contatin a list. 

```
monitors:
  - first monitor
  - second monitor
  - third monitor
```

Each element of this list must respect a schema.

## Monitor element 

This element is a dict that will contain several options both mandatory and optional:

Key: **broker** *(required)*
Address of the broker

Key: **port** *(required)*
Port of the broker 
default: 1883


* username: Username to authenticate with the broker [default: no authentication]
* password**: Password of the set username to authenticate with the broker
* name*: Name of the computer to monitor, you can choose it as you want (there isn't a correct value)
* mqtt_id: If your broker wants a specific mqtt id, it can be set from here [default: name options will be used]
* send_interval*: Interval of seconds between sending two sensors' data
* debug: Log more information such as topic subscription and data send events [default: False]
* sensors*: List of sensors to enable - check the following pages
* commands*: List of commands to enable - check the following pages

\* Mandatory field

\** Password field is mandatory only if username is set