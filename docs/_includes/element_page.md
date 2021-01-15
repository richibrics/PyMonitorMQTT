{% include navigation.html %}

{% assign element_name = page.url | split: "/" | last | split: "." | first %}  

{% for entry in site.data.sensors.data %}
    {% if entry.name == element_name %}
        {% assign element = entry %}
        {% assign type = "sensor" %}
    {% endif %}
{% endfor %}

{% if type == "sensor" %}
# {{ element.name }} Sensor
{% else %}
# {{ element.name }} Commands
{% endif %}

{{element.long_description}}

## Compatibility

<div style="margin: 0 0 0 0;">
{% if element.compatibility contains "m" %}
<li>macOS</li>
{% endif %}
{% if element.compatibility contains "l" %}
<li>Linux</li>
{% endif %}
{% if element.compatibility contains "w" %}
<li>Windows</li>
{% endif %}
</div>

{% if element.topics %}
## Data and Topics

{% include list_topics.html element=element %}
    
{% endif %}

{% if element.config %}
## Configuration

{% include list_keys.html config=element.config %}

{% endif %}

