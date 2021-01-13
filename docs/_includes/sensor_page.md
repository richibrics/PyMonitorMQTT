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

{% include list_topics_sensor.html sensor=sensor %}
    
{% endif %}

{% if sensor.config %}
## Configuration

{% include list_keys_sensor.html sensor=sensor %}

{% endif %}


{% if sensor.extra %}
## Additional information 
 
{% assign extra_names = sensor.extra %}
    {% for name in extra_names %}
        {% assign extra_import = "data/sensors/" | append: sensor.name | append: "/extra/" | append: name | append: ".md" %}
{% include {{extra_import}} %}
    {% endfor %}
{% endif %}



