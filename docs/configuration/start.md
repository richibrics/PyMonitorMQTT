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

- **broker** *(**required**)*
> Address of the broker

- **name** *(**required**)*
> Name of the computer to monitor, you can choose it as you want (there isn't a correct value)

- **send_interval** *(**required**)*
> Interval of seconds between sending two sensors' data

- **port** *(optional, default: 1883)*
> Port of the broker 

- **username** *(optional)*
> Username to authenticate with the broker [default: no authentication]

- **password** *(optional, required if you added an username)*
> Password of the set username to authenticate with the broker

- **mqtt_id** *(optional)*
> If your broker wants a specific mqtt id, it can be set from here [default: name options will be used]

- **debug** *(optional, default: False)*
> Log more information such as topic subscription and data send events [default: False]

- **sensors** *(optional)*
> List of sensors to enable

- **commands** *(optional)*
> List of commands to enable
