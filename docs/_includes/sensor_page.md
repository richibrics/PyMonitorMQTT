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

<div style="margin: 0 0 0 0;">
{% if sensor.compatibility contains "m" %}
<li>macOS</li>
{% endif %}
{% if sensor.compatibility contains "l" %}
<li>Linux</li>
{% endif %}
{% if sensor.compatibility contains "w" %}
<li>Windows</li>
{% endif %}
</div>

{% if sensor.topics %}
## Data and Topics

    {% for topic in sensor.topics %}

        {% if topic.type and topic.additional == "extra" %}
            {% assign type = "Additional" %}
        {% else %}
            {% assign type = "Basic" %}
        {% endif %}

#### {{topic.topic}}


> Type: {{type}}
{{topic.description}}
    {% endfor %}

{% endif %}

{% if sensor.extra %}
## Additional information

{{sensor.extra}}
{% endif %}

{% if sensor.config %}
## Configuration

{% include list_keys_sensor.html sensor=sensor %}

{% endif %}


{% assign example_data = site.data.sensors.examples[sensor_name] %}
{% if example_data and example_data.size > 0 %}
    {% if example_data.size == 1 %}
## Example
    {% else %}
## Examples
    {% endif %}

{% if example.title %}
#### {{example.title}}
{% endif %}

{% if example.comment %}
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
### {{extra.title}}

{{extra.text}}
    {% endfor %}
{% endif %}



