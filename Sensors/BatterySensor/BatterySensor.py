import psutil
from Sensors.Sensor import Sensor


TOPIC_PERCENTAGE = 'battery_level_percentage'
TOPIC_CHARGING_STATUS = 'battery_charging'


class BatterySensor(Sensor):
    def Initialize(self):
        self.AddTopic(TOPIC_PERCENTAGE)
        self.AddTopic(TOPIC_CHARGING_STATUS)

    def Update(self):
        batteryInfo = self.GetBatteryInformation()
        self.SetTopicValue(TOPIC_PERCENTAGE, batteryInfo['level'])
        self.SetTopicValue(TOPIC_CHARGING_STATUS, str(batteryInfo['charging']))

    def GetBatteryInformation(self):
        battery = psutil.sensors_battery()
        if battery:  # Then the device has a battery
            return {'level': battery.percent, 'charging': battery.power_plugged}
        else:
            return {'level': 'None', 'charging': 'None'}
