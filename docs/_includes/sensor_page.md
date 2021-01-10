{% include navigation.html %}

{% assign sensor_name = page.url | split: "/" | last | split: "." | first %}  

{% for entry in site.data.sensors.data %}
    {% if entry.name == sensor_name %}
        {% assign sensor = entry %}
    {% endif %}
{% endfor %}

# {{ sensor.name }} Sensor

{{sensor.long_description}}

**Compatible OS:**

{% if sensor.compatibility contains "m" %}
* macOS
{% endif %}
{% if sensor.compatibility contains "l" %}
* Linux
{% endif %}
{% if sensor.compatibility contains "w" %}
* Windows
{% endif %}

## Configuration

{% include table_keys_sensor.html sensor=sensor %}



{% assign example_data = site.data.sensors.examples[sensor_name] %}
{% if example_data %}
    {% if example_data.size == 1 %}
## Example
    {% else %}
## Examples
    {% endif %}

    {% for example in example_data %}
```
{{example}}
```
    {% endfor %}
{% endif %}





## Data and Topics



{% if sensor.extra %}
## Additional information

{{sensor.extra}}
{% endif %}