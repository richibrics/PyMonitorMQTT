from consts import *
import math
from Configurator import Configurator as cf

# Value formatter
# If I have to return value not in byte but with MB/GB/KB; same for time

# OPTIONS MEANING (example with byte values)
# size: True "means that will be used the nearest unit 1024Byte->1KB" False "send the value without using the pow1024 mechianism"
# size: MB "means that will be used the specified size 2014Byte->0.001MB"
# unit_of_measurement: True/False "if you want to add the unit at the end of the value"
# decimals: integer "the number of decimal to leave to the value"


class ValueFormatter():
    TYPE_NONE = 0
    TYPE_BYTE = 1
    TYPE_TIME = 2
    TYPE_PERCENTAGE = 3
    TYPE_FREQUENCY = 4

    @staticmethod
    def GetFormattedValue(value, valueType, options=None):
        if options==None:
            options=ValueFormatter.Options() # Default will be used
            
        if valueType == ValueFormatter.TYPE_NONE:  # No edit needed
            return value
        elif valueType == ValueFormatter.TYPE_BYTE:
            return ValueFormatter.ByteFormatter(value,options)
        elif valueType == ValueFormatter.TYPE_TIME:
            return ValueFormatter.TimeFormatter(value, options)
        elif valueType == ValueFormatter.TYPE_FREQUENCY:
            return ValueFormatter.FrequencyFormatter(value, options)
        elif valueType == ValueFormatter.TYPE_PERCENTAGE:
            if cf.GetOption(options,VALUEFORMATTER_OPTIONS_UNIT_OF_MEASUREMENT_KEY,VALUEFORMATTER_OPTIONS_UNIT_OF_MEASUREMENT_DEFAULT):
                return str(value) + '%'
            else:
                return value
        else:
            return value
 
    # Get from number of bytes the correct byte size: 1045B is 1KB. If size_wanted passed and is SIZE_MEGABYTE, if I have 10^9B, I won't diplay 1GB but c.a. 1000MB   
    @staticmethod
    def ByteFormatter(value,options):
        # Get value in bytes
        asked_size = cf.GetOption(options,VALUEFORMATTER_OPTIONS_SIZE_KEY)
        decimals = cf.GetOption(options,VALUEFORMATTER_OPTIONS_DECIMALS_KEY)
        
        if asked_size and asked_size in BYTE_SIZES:
            powOf1024 = BYTE_SIZES.index(asked_size)
        else:
            powOf1024 = math.floor(math.log(value, 1024))

        result = str(round(value/(math.pow(1024, powOf1024)), decimals))

        # Add unit
        if cf.GetOption(options,VALUEFORMATTER_OPTIONS_UNIT_OF_MEASUREMENT_KEY,VALUEFORMATTER_OPTIONS_UNIT_OF_MEASUREMENT_DEFAULT):
            result = result + BYTE_SIZES[powOf1024]
    
        return result

    @staticmethod
    def TimeFormatter(value, options):
        # Get value in milliseconds
        result=value
        # Add unit
        if cf.GetOption(options,VALUEFORMATTER_OPTIONS_UNIT_OF_MEASUREMENT_KEY,VALUEFORMATTER_OPTIONS_UNIT_OF_MEASUREMENT_DEFAULT):
            result = str(value) + 'ms'
        return result

    @staticmethod
    def FrequencyFormatter(value, options):
        # Get value in hertz
        result=value
        # Add unit
        if cf.GetOption(options,VALUEFORMATTER_OPTIONS_UNIT_OF_MEASUREMENT_KEY,VALUEFORMATTER_OPTIONS_UNIT_OF_MEASUREMENT_DEFAULT):
            result = str(value) + 'hz'
        return result

    @staticmethod
    def Options(decimals=VALUEFORMATTER_OPTIONS_DECIMALS_DEFAULT ,add_unit_of_measurement=VALUEFORMATTER_OPTIONS_UNIT_OF_MEASUREMENT_DEFAULT, adjust_size=VALUEFORMATTER_OPTIONS_SIZE_DEFAULT):
        return {VALUEFORMATTER_OPTIONS_DECIMALS_KEY: decimals, VALUEFORMATTER_OPTIONS_UNIT_OF_MEASUREMENT_KEY: add_unit_of_measurement, VALUEFORMATTER_OPTIONS_SIZE_KEY:adjust_size}

    #def