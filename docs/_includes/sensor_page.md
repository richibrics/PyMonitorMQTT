{% include navigation.html %}

{% assign sensor_name = page.url | split: "/" | last | split: "." | first %}  

{% for entry in site.data.sensors.data %}
    {% if entry.name == sensor_name %}
        {% assign sensor = entry %}
    {% endif %}
{% endfor %}

# {{ sensor.name }} Sensor

{{sensor.long_description}}

## Compatibility

{% if sensor.compatibility contains "m" %}
* macOS
{% endif %}
{% if sensor.compatibility contains "l" %}
* Linux
{% endif %}
{% if sensor.compatibility contains "w" %}
* Windows
{% endif %}



## Data and Topics



{% if sensor.extra %}
## Additional information

{{sensor.extra}}
{% endif %}

## Configuration

{% include table_keys_sensor.html sensor=sensor %}


{% assign example_data = site.data.sensors.examples[sensor_name] %}
{% if example_data and example_data.size > 0 %}
    {% if example_data.size == 1 %}
## Example
    {% else %}
## Examples
    {% endif %}

{% if {{example.title}} %}
#### {{example.title}}
{% endif %}

{% if {{example.comment}} %}
{{example.comment}}
{% endif %}

    {% for example in example_data %}
```
{{example.example}}
```
    {% endfor %}
{% endif %}

{% assign additional_data = site.data.sensors.extra[sensor_name] %}
{% if additional_data and additional_data.size > 0 %}
## Additional information

    {% for extra in additional_data %}
### {{extra.example}}

{{extra.text}}
    {% endfor %}
{% endif %}



