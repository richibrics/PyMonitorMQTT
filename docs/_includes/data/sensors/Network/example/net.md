## Example

In this example I set different parameters:

- **value_format**: I personally prefer to read traffic data as MB and not as B so I set the 'size' to MB and also without decimals
- **discovery**: I told that I want values in MB so when the remote Hub receives the data, must know the new unit_of_measurement to work properly and not log data as B
- **exclude_interfaces**: The 'lo' interfaces is the loopback interface and I don't need information about that, also for the VirtualBox adapter
- **rename_interfaces**: I use my system in dual-boot with Linux and Windows so my wireless interface has 2 different names. I set the linux wireless adapter name (wlp0s20f3) to the windows adapter name (Wi-Fi) to have a single sensor in my smart-hub

```
      - Network:
          discovery:
            settings:
              - topic: "network/traffic/bytes_recv"
                unit_of_measurement: MB  
              - topic: "network/traffic/bytes_sent"
                unit_of_measurement: MB  
          value_format: 
            size: MB # for traffic
            decimals: 0
          contents:
            exclude_interfaces:
              - lo
              - VirtualBox Host-Only Network
            rename_interfaces:
              wlp0s20f3: Wi-Fi
```