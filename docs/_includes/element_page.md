{% include navigation.html %}

{% assign url_data = page.url | split: "/" | reverse %}
{% assign element_name = url_data | first | split: "." | first %}  
{% assign element_type = url_data %}  

{{element_name}}
{{ page.url | split: "/"}}

{% for entry in site.data.sensors.data %}
    {% if entry.name == element_name %}
        {% assign element = entry %}
        {% assign type = "sensor" %}
    {% endif %}
{% endfor %}

{% if type == "sensor" %}
# {{ element.name }} Sensor
{% else %}
# {{ element.name }} Command
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


{% if element.default and element.default.example_custom_topic %}
    {% assign example_count = 1 %}
{% else %}
    {% assign example_count = 0 %}
{% endif %} 

{% if element.examples %}
    {% assign example_count = example_count | plus: element.examples.size %}
{% endif %} 

{% if example_count >0 %}
    {% if example_count == 1 %}
## Example
    {% else %}
## Examples
    {% endif %} 
 
{% if element.default and element.default.example_custom_topic %}
{% if type == "sensor" %}
{% include data/sensors/default/example_custom_topic.md sensor=element topic=element.default.example_custom_topic %}
{% else %}
{% include data/commands/default/example_custom_topic.md command=element topic=element.default.example_custom_topic %}
{% endif %}
{% endif %}

{% assign example_names = element.examples %}
    {% for name in example_names %}
    {% if type == "sensor" %}
        {% assign example_import = "data/sensors/" | append: element.name | append: "/examples/" | append: name | append: ".md" %}
    {% else %}
        {% assign example_import = "data/commands/" | append: element.name | append: "/examples/" | append: name | append: ".md" %}
    {% endif %}
{{example_import}}
    {% endfor %}
{% endif %} 


{% if element.extra %}
## Additional information 
 
{% assign extra_names = element.extra %}
    {% for name in extra_names %}
        {% if type == "sensor" %}    
        {% assign extra_import = "data/sensors/" | append: element.name | append: "/extra/" | append: name | append: ".md" %}
        {% else %}
        {% assign extra_import = "data/commands/" | append: element.name | append: "/extra/" | append: name | append: ".md" %}
    {% endif %}
{{extra_import}}
    {% endfor %}
{% endif %}



