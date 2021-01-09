{% include navigation.html %}

{% assign sensor_name = page.url | split: "/" | last | split: "." | first %}  

{% for sensor in site.data.sensors %}



{% endfor %}

ora da sensor_name prendo il sensor da data e da lì riempio tutto, sì pure il titolo

# {{ sensor_name }} Sensor

Try