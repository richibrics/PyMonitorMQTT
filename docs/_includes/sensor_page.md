{% include navigation.html %}

{% assign sensor_name = page.url | split: "/" | last | split: "." | first %}  

{% for entry in site.data.sensors %}

    {% if entry.name == sensor_name %}

        {% assign sensor = entry %}

    {% endif %}

{% endfor %}

ora da sensor_name prendo il sensor da data e da lì riempio tutto, sì pure il titolo

# {{ sensor.name }} Sensor

Try