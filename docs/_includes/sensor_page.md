{% include navigation.html %}

{% assign sensor_name = page.url | split: "/" | last | split: "." | first %}  

{% for entry in site.data.sensors %}
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

{% include table_keys_sensor.html yaml=sensor %}