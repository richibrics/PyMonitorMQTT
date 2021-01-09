{% include navigation.html %}

{{page.url}}
{% assign sensor_name = page.url | split: "/" | first %}  

# {{ sensor_name }} Sensor

Try