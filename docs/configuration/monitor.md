{% include navigation.html %}

# Monitor element 

This element is a dict that will contain several options both mandatory and optional (order isn't relevant)

- **broker**
> Address of the broker

- **name**
> Name of the computer to monitor, you can choose it as you want (there isn't a correct value)

- **sensors** 
> List of sensors to enable

- **commands**
> List of commands to enable

- **send_interval**
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

## Example

EXAMPLE HERE
