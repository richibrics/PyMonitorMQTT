{% include navigation.html %}

# YAML root

In the root of the configuration.yaml file you can place these configuration keys:

{% include table_keys.html yaml='root' %}

## Schema

```
monitors:
  - first monitor
  - second monitor
  - third monitor

logger_message_width: integer
```

## Example

```
logger_message_width: 55

monitors:
  - broker: mqtt.eclipse.org
    name: MyLenovo
    username: myuser
    password: mypass
    send_interval: 600 # 10 minutes 

    sensors:
      - Ram
      - Disk
      - DesktopEnvironment
      - Cpu
      - Brightness
      - FileRead:
          contents:
            filename: "/home/plex/movielist.txt"
      
    commands:
      - Brightness
      - Notify:
          custom_topics:
            - notify_system/leave
          contents:
            message: 'It's time to leave !'
```