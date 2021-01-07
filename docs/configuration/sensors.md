{% include navigation.html %}

# Sensors

This monitor uses sensors, created ad-hoc for each operating system, that take data from the system it's working on and sends them to the broker.

These sensors can be enabled and customized whenever you want: to activate a sensor you only have to place it's name (the part of the name before 'Sensor') in the 'sensors' key list.

## Available sensors

{% include table_elements.html yaml='sensors' %}