{% include navigation.html %}

# Global configuration

In the root of the configuration.yaml file you can place all these configuration keys:

TO WRITE
...............


## Example

EXAMPLE HERE


OLD PART: 

PyMonitorMQTT supports more than one broker connection simultaneously. Each monitor configuration must be placed in the 'monitors' key that will contain a list. 

```
monitors:
  - first monitor
  - second monitor
  - third monitor
```

Each element of this list must respect a schema.