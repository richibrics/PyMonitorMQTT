{% include navigation.html %}

{{page.url}}
{% assign sensor_name = page.url | split: "/" | last | split: "." | first %}  

# {{ sensor_name }} Sensor

Try