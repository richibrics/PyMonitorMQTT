{% include navigation.html %}

{{page.url}}
{% assign sensor_name = page.url | split: "/" | last | split: "." | first %}  
ora da sensor_name prendo il sensor da data e da lì riempio tutto, sì pure il titolo
# {{ sensor_name }} Sensor

Try