{% include navigation.html %}

# Monitor element 

This element is a dict that will contain several options both mandatory and optional (order isn't relevant)

{% include table_keys.html yaml='monitor' %}

## Example

```
  - broker: mqtt.eclipse.org
    name: Lenovo
    username: example
    password: secret
    send_interval: 20 # Seconds

    debug: True

    sensors:
      - CpuTemperatures
      - Time


    commands:
      - Shutdown
      - Reboot
```
