import psutil
from Entity import Entity


TOPIC_PERCENTAGE = 'battery/battery_level_percentage'
TOPIC_CHARGING_STATUS = 'battery/battery_charging'


class BatterySensor(Entity):
    def Initialize(self):
        self.AddTopic(TOPIC_PERCENTAGE)
        self.AddTopic(TOPIC_CHARGING_STATUS)

    def Update(self):
        batteryInfo = self.GetBatteryInformation()
        self.SetTopicValue(TOPIC_PERCENTAGE, batteryInfo['level'],self.ValueFormatter.TYPE_PERCENTAGE)
        self.SetTopicValue(TOPIC_CHARGING_STATUS, str(batteryInfo['charging']))

    def GetBatteryInformation(self):
        battery = psutil.sensors_battery()
        if battery:  # Then the device has a battery
            return {'level': battery.percent, 'charging': battery.power_plugged}
        else:
            return {'level': 'None', 'charging': 'None'}
