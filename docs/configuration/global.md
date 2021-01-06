{% include navigation.html %}

# YAML root

In the root of the configuration.yaml file you can place all these configuration keys:

{% include config_list.html yaml='conf_root' %}

## Schema

```
monitors:
  - first monitor
  - second monitor
  - third monitor

logger_message_width: 55
```

## Example

```
monitors:
  - broker: mqtt.eclipse.org
    name: MyLenovo
    username: myuser
    password: mypass
    send_interval: 600 # 10 minutes 

    sensors:
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


  - broker: mqtt.example.com
    name: Lenovo
    send_interval: 20 # seconds

    sensors:
      - Os
      - Ram
      - Disk
      - DesktopEnvironment
      - Cpu
      - Brightness
      - Battery
      - CpuTemperatures
      - Network
      - Screenshot
      - Time


    commands:
      - Shutdown
      - Lock
      - Reboot
      - Brightness
      - Sleep
      - TurnOffMonitors
      - TurnOnMonitors
```