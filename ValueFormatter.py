from consts import *
import math

# Value formatter
# If I have to return value not in byte but with MB/GB/KB; same for time


class ValueFormatter():
    TYPE_NONE = 0
    TYPE_BYTE = 1
    TYPE_TIME = 2
    TYPE_PERCENTAGE = 3
    TYPE_FREQUENCY = 4

    def GetFormattedValue(value, valueType, decimals=FORMATTED_VALUE_DECIMALS):
        if valueType is None or valueType == ValueFormatter.TYPE_NONE:  # No edit needed
            return value
        elif valueType == ValueFormatter.TYPE_BYTE:
            return ValueFormatter.ByteFormatter(value, decimals)
        elif valueType == ValueFormatter.TYPE_TIME:
            return ValueFormatter.TimeFormatter(value, decimals)
        elif valueType == ValueFormatter.TYPE_FREQUENCY:
            return ValueFormatter.FrequencyFormatter(value, decimals)
        elif valueType == ValueFormatter.TYPE_PERCENTAGE:
            return str(value) + '%'
        else:
            return value

    def ByteFormatter(value, decimals):
        # Get value in bytes
        powOf1024 = math.floor(math.log(value, 1024))
        size = round(value/(math.pow(1024, powOf1024)), decimals)
        result = str(size) + BYTE_SIZES[powOf1024]
        return result

    def TimeFormatter(value, decimals):
        # Get value in milliseconds
        result = str(value) + 'ms'
        return result

    def FrequencyFormatter(value, decimals):
        # Get value in hertz
        result = str(value) + 'hz'
        return result
