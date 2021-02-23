class BitOptions():

    @staticmethod
    def SetOptions(list_of_entries, default_starting_options=0):
        options = default_starting_options
        for option in list_of_entries:
            options+=option
        return options

    @staticmethod
    def AddToOptions(options, list_of_entries):
        for option in list_of_entries:
            options+=option
        return options

    @staticmethod
    def GetBitList(options):
        # return bit from options number
        bit = "{0:b}".format(options)
        return [int(char) for char in bit] 

    @staticmethod
    def CheckOption(options, option): # Option is the bit number from left (1=bit on the right LSB)\
        bit = BitOptions.GetBitList(options)
        size = len(bit)
        if(options <= size):
            if options[size-option] == 1:
                return True
        return False