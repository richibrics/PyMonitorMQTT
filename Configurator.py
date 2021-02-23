from consts import *

class Configurator():
    # Returns the value of the option I find using the path from a passed config
    # Can also return a value (that you can pass to the fucntion) if it can't find the path 
    @staticmethod
    def GetOption(config, path, defaultReturnValue=None):
        try:
            searchConfigTree=config
            
            # if in options I have a value for that option rerturn that else return False
            if type(path) == str:
                if searchConfigTree is not None and path in searchConfigTree:
                    return searchConfigTree[path]
                else:
                    return defaultReturnValue

            elif type(path) == list:  # It's a list with the option Path like contents -> values -> first
                while (path and len(path)):
                    if searchConfigTree is None:
                        return defaultReturnValue
                    current_option = path.pop(0)
                    if type(searchConfigTree) == dict and current_option in searchConfigTree:
                        searchConfigTree = searchConfigTree[current_option]
                    else:
                        return defaultReturnValue  # Not found
                return searchConfigTree  # All ok, found
            else:
                raise Exception(
                    "Error during GetOption: option type not valid " + str(type(path)))
        except Exception as e:
            raise Exception(e)
    
    @staticmethod
    def ReturnAsList(configuration, noneCondition=None): 
        # If the configuration passed is a list, return it, else place configuration in a list and return the list 
        # PS if configuration passed equals to noneCondition, don't return the list but the noneCondition
        if configuration==noneCondition:
            return noneCondition
        if type(configuration) == list:
            return configuration
        else:
            return [configuration]