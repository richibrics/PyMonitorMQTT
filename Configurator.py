from consts import *

class Configurator():
    def __init__(self,config):
        self.configuration = config

    # Returns the value of the option I find using the path from full configuration or from 
    # a sub config ('startConfig').
    # Can also return a value (that you can pass to the fucntion) if it can't find the path 
    def GetOption(self, path, startConfig=None, defaultReturnValue=None):
        # If i have a subconfig dict where I have to start the options search I use it
        if startConfig is not None:
            searchConfigTree = startConfig
        else: # else I use the full configuration to search
            searchConfigTree=self.configuration


        # if in options I have a value for that option rerturn that else return False
        if type(path) == str:
            if path in searchConfigTree:
                return searchConfigTree[path]
            else:
                return defaultReturnValue

        elif type(path) == list:  # It's a list with the option Path like contents -> values -> first
            while (len(path)):
                current_option = path.pop(0)
                if type(searchConfigTree) == dict and current_option in searchConfigTree:
                    searchConfigTree = searchConfigTree[current_option]
                else:
                    return defaultReturnValue  # Not found
            return searchConfigTree  # All ok, found
        else:
            raise Exception(
                "Error during GetOption: option type not valid " + str(type(option)))
